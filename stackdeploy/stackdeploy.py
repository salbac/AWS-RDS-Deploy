import sys

import boto3
import botocore.exceptions

# TODO Configure acces for specific IP restriction with sg
# TODO Unit Test and coverage


class StackDeploy(object):

    def __init__(self):
        self.aws_token = None
        self.aws_acces = None
        self.aws_secret = None
        self.aws_region = None
        self.auth_type = None

    def aws_client(self, auth_type):
        if auth_type == 'AWS Token':
            try:
                self.ec2 = boto3.client('ec2',
                                        aws_session_token=self.aws_token,
                                        region_name=self.aws_region,
                                        )
                self.ec2.describe_account_attributes()
            except botocore.exceptions.ClientError as err:
                print('[*] {}'.format(err))
                sys.exit(1)
            try:
                self.rds = boto3.client('rds',
                                        aws_session_token=self.aws_token,
                                        region_name=self.aws_region,
                                        )
                self.rds.describe_account_attributes()
            except botocore.exceptions.ClientError as err:
                print('[*] {}'.format(err))
                sys.exit(1)

        elif auth_type == 'AWS Key':
            try:
                self.ec2 = boto3.client('ec2',
                                        aws_access_key_id=self.aws_acces,
                                        aws_secret_access_key=self.aws_secret,
                                        region_name=self.aws_region,
                                        )
                self.ec2.describe_account_attributes()
            except botocore.exceptions.ClientError as err:
                print('[*] {}'.format(err))
                sys.exit(1)
            try:
                self.rds = boto3.client('rds',
                                        aws_access_key_id=self.aws_acces,
                                        aws_secret_access_key=self.aws_secret,
                                        region_name=self.aws_region,
                                        )
                self.rds.describe_account_attributes()
            except botocore.exceptions.ClientError as err:
                print('[*] {}'.format(err))
                sys.exit(1)

    def get_vpcs(self):
        v = []
        vpcs = self.ec2.describe_vpcs()
        if vpcs['Vpcs']:
            for vpc in vpcs['Vpcs']:
                if 'Tags' in vpc:
                    for tag in vpc['Tags']:
                        if tag['Key'] == 'Name':
                            name = tag['Value']
                            v.append({'name': 'Vpc Name {}, Vpc Id {}'.format(name, vpc['VpcId'])})
                        else:
                            v.append({'name': 'Vpc Name {}, Vpc Id {}'.format('', vpc['VpcId'])})
                else:
                    v.append({'name': 'Vpc Name {}, Vpc Id {}'.format('', vpc['VpcId'])})
            return v

    def get_sg_from_vpc(self, vpc):
        s = []
        sgs = self.ec2.describe_security_groups(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        vpc
                    ]
                }
            ]
        )
        for sg in sgs['SecurityGroups']:
            s.append({'name': 'SG Name {}, SG Id {}'.format(sg['GroupName'], sg['GroupId'])})
        return s

    def get_db_subnet_group(self, vpc):
        db_subnet = self.rds.describe_db_subnet_groups()
        dbsg = []
        for r in db_subnet['DBSubnetGroups']:
            if r['VpcId'] == vpc:
                dbsg.append({'name': r['DBSubnetGroupName']})
        return dbsg

    def create_db_subnet_group(self, vpc, name):
        vpc_subnets = self.ec2.describe_subnets()
        subnetids = []
        for subnet in vpc_subnets['Subnets']:
            if subnet['VpcId'] == vpc:
                subnetids.append(subnet['SubnetId'])
        if subnetids:
            response = self.rds.create_db_subnet_group(
                DBSubnetGroupName='dbsg-{}'.format(name),
                DBSubnetGroupDescription='DB Subnet for {}'.format(vpc),
                SubnetIds=subnetids
            )
            return [{'name': response['DBSubnetGroup']['DBSubnetGroupName']}]
        else:
            print('[*] Please review your subnet configuration for Vpc-Id {}'.format(vpc))
            sys.exit(1)

    def get_az_from_db_subnet_group(self, dbsname):
        response = self.rds.describe_db_subnet_groups(
            DBSubnetGroupName=dbsname
        )
        availabilityzone = []
        for res in response['DBSubnetGroups'][0]['Subnets']:
            availabilityzone.append(res['SubnetAvailabilityZone']['Name'])
        return availabilityzone

    def get_rds_engines(self):
        versions = []
        if self.auth_type == 'AWS Token':
            try:
                client = boto3.client('rds',
                                      aws_session_token=self.aws_token,
                                      )
                client.describe_account_attributes()
            except botocore.exceptions.ClientError as err:
                print('[*] {}'.format(err))
                sys.exit(1)
        elif self.auth_type == 'AWS Key':
            try:
                client = boto3.client('rds',
                                      aws_access_key_id=self.aws_acces,
                                      aws_secret_access_key=self.aws_secret,
                                      )
                client.describe_account_attributes()
            except botocore.exceptions.ClientError as err:
                print('[*] {}'.format(err))
                sys.exit(1)
        paginator = client.get_paginator('describe_db_engine_versions')
        pages = paginator.paginate()
        for page in pages:
            for obj in page['DBEngineVersions']:
                e = {'Engine': obj['Engine'],
                     'Version': obj['EngineVersion'],
                     'ParameterGroupFamily': obj['DBParameterGroupFamily']}
                versions.append(e)
        return versions

    def get_rds_major_engines(self, engines):
        result = []
        engine_vendors = []
        for engine in engines:
            engine_vendors.append(engine['Engine'])
        engines = set(engine_vendors)
        for engine in sorted(engines):
            # TODO unlock all engines in rds
            if engine.startswith('oracle'):
                result.append({'name': engine})
        return result

    def get_rds_minor_engine_version(self, engine, versions):
        minor_versions = []
        for version in versions:
            if version['Engine'] == engine:
                minor_versions.append({'name': version['Version']})
        return minor_versions

    def get_rds_parameter_group_family(self, engines, engine, version):
        for e in engines:
            if e['Engine'] == engine['engine_type'] and e['Version'] == version['engine_version']:
                return e['ParameterGroupFamily']

    def rds_instance_is_available(self):
        waiter = self.rds.get_waiter('db_instance_available')
        try:
            waiter.wait()
            print("[*] Instance created")
        except botocore.exceptions.WaiterError as e:
            if "Max attempts exceded" in e.message:
                print("[*] Error Max attempts exceded")
                sys.exit(1)
            else:
                print(e)

    def create_rds_parameter_group(self, name, instance, family):
        new_parameter_group = self.rds.create_db_parameter_group(
            DBParameterGroupName=name,
            Description='Parameter group for instance {}'.format(instance),
            DBParameterGroupFamily=family
        )
        if new_parameter_group['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("[*] Creating parameter group")

    def modify_parameter(self, parameter_group, data):
        for key in data.keys():
            modify_parameter = self.rds.modify_db_parameter_group(
                DBParameterGroupName=parameter_group,
                Parameters=[
                    {
                        'ParameterName': key,
                        'ParameterValue': data[key],
                        'ApplyMethod': 'immediate',
                    },
                ]
            )
            if modify_parameter['ResponseMetadata']['HTTPStatusCode'] == 200:
                print("[*] Modifing parameter group")

    def create_rds_instance(self, data):
        new_instance = self.rds.create_db_instance(
            DBName=data['DBName'],
            DBInstanceIdentifier=data['DBInstanceIdentifier'],
            AllocatedStorage=data['AllocatedStorage'],
            DBInstanceClass=data['DBInstanceClass'],
            Engine=data['Engine'],
            MasterUsername=data['MasterUsername'],
            MasterUserPassword=data['MasterUserPassword'],
            DBSubnetGroupName=data['DBSubnetGroupName'],
            VpcSecurityGroupIds=[
                data['VpcSecurityGroupIds'],
            ],
            AvailabilityZone=data['AvailabilityZone'],
            # PreferredMaintenanceWindow='string',
            DBParameterGroupName=data['DBParameterGroupName'],
            BackupRetentionPeriod=7,
            # PreferredBackupWindow='string',
            Port=data['Port'],
            MultiAZ=data['MultiAZ'],
            EngineVersion=data['EngineVersion'],
            AutoMinorVersionUpgrade=False,
            LicenseModel=data['LicenseModel'],
            # Iops=123,
            # OptionGroupName='default:oracle-se1-11-2',
            CharacterSetName=data['CharacterSetName'],
            PubliclyAccessible=data['PubliclyAccessible'],
            # Tags=[
            #     {
            #         'Key': 'Environment',
            #         'Value': 'PRO'
            #     },
            # ],
            # DBClusterIdentifier='string',
            StorageType=data['StorageType'],
            # TdeCredentialArn='string',
            # TdeCredentialPassword='string',
            StorageEncrypted=data['StorageEncrypted'],
            # KmsKeyId='string',
            # Domain='string',
            # CopyTagsToSnapshot=True,
            MonitoringInterval=0,
            # MonitoringRoleArn='string',
            # DomainIAMRoleName='string',
            # PromotionTier=123,
            # Timezone='string',
            EnableIAMDatabaseAuthentication=False,
            EnablePerformanceInsights=True,
            # PerformanceInsightsKMSKeyId='string',
            PerformanceInsightsRetentionPeriod=7,
            # EnableCloudwatchLogsExports=[
            #     'string',
            # ],
            # ProcessorFeatures=[
            #     {
            #         'Name': 'string',
            #         'Value': 'string'
            #     },
            # ],
            DeletionProtection=False,
            # MaxAllocatedStorage=20
        )
        if new_instance['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("[*] Creating instance")

    def get_instance_types(self):
        allowed_family = ['db.m5.', 'db.m4.', 'db.m3.', 'db.m1.', 'db.z1d.', 'db.x1e.', 'db.x1.', 'db.r5.', 'db.r4.',
                          'db.r3.', 'db.m2.', 'db.t3.', 'db.t2.']
        paginator = self.ec2.get_paginator('describe_instance_types')
        pages = paginator.paginate()
        instances = []
        for page in pages:
            for instance in page['InstanceTypes']:
                for family in allowed_family:
                    if 'db.{}'.format(instance['InstanceType']).startswith(family):
                        instances.append('db.{}'.format(instance['InstanceType']))
        res = []
        for ins in sorted(instances):
            res.append({'name': ins})
        return res

    def get_regions(self):
        region_list = []
        if self.auth_type == 'AWS Token':
            try:
                client = boto3.client('ec2',
                                      aws_session_token=self.aws_token,
                                      )
                client.describe_account_attributes()
            except botocore.exceptions.ClientError as err:
                print('[*] {}'.format(err))
                sys.exit(1)
        elif self.auth_type == 'AWS Key':
            try:
                client = boto3.client('ec2',
                                      aws_access_key_id=self.aws_acces,
                                      aws_secret_access_key=self.aws_secret,
                                      )
                client.describe_account_attributes()
            except botocore.exceptions.ClientError as err:
                print('[*] {}'.format(err))
                sys.exit(1)
        regions = client.describe_regions()
        for region in regions['Regions']:
            region_list.append({'name': region['RegionName']})
        return region_list

    # # Not implemented
    # def create_db_security_group(self, name):
    #     new_sg = self.rds.create_db_security_group(
    #         DBSecurityGroupName='sg-{}'.format(name),
    #         DBSecurityGroupDescription='SG for instance {}.'.format(name)
    #     )
    #     if new_sg['ResponseMetadata']['HTTPStatusCode'] == 200:
    #         print("[*] Creating new DB security group")
    #     return new_sg['DBSecurityGroup']['DBSecurityGroupName']
