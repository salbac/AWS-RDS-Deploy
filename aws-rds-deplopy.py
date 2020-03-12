#!/usr/bin/env python3

import os
from cli.cli import Cli
from stackdeploy.stackdeploy import StackDeploy

DEBUG = os.environ['DEBUG']
TOKEN = os.environ['AWS_TOKEN']
ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
SECRET_KEY = os.environ['AWS_SECRET_KEY']

if __name__ == "__main__":

    # Create cli object
    cli = Cli()

    # Create sd object
    sd = StackDeploy()

    # Ask for auth type and set credentials
    aws_auth = cli.ask_for_aws_auth_type()
    sd.auth_type = aws_auth['auth_type']
    if aws_auth['auth_type'] == 'AWS Token':
        if DEBUG:
            sd.aws_token = TOKEN
        else:
            sd.aws_token = aws_auth['aws_token']
    elif aws_auth['auth_type'] == 'AWS Key':
        if DEBUG:
            sd.aws_acces = ACCESS_KEY
            sd.aws_secret = SECRET_KEY
        else:
            sd.aws_acces = aws_auth['aws_access_key']
            sd.aws_secret = aws_auth['aws_secret_key']

    # Get AWS available regions
    regions = sd.get_regions()

    # Ask for region to deploy
    sd.aws_region = cli.ask_for_region(regions)

    # Set up EC2 and RDS client in sd object
    sd.aws_client(aws_auth['auth_type'])

    # Ask for RDS information
    rds_data = cli.ask_for_rds_data()
    storage = cli.ask_for_storage()

    # Select engine version
    print('[*] Getting available engine versions, please wait.')
    engines = sd.get_rds_engines()
    engine_version = cli.ask_for_engine(
        sd.get_rds_major_engines(engines)
    )
    minor_version = cli.ask_for_engine_version(
        sd.get_rds_minor_engine_version(engine_version['engine_type'], engines)
    )

    # Get AWS Vpcs in the selected region
    vpcs = sd.get_vpcs()
    vpc = cli.ask_for_vpcs(vpcs)
    vpcid = vpc['vpc'].split('Vpc Id ')[1]

    # Get AWS Security Groups for selected Vpc
    sgs = sd.get_sg_from_vpc(vpcid)
    sg = cli.ask_for_sg(sgs)
    sgid = sg['sg'].split('SG Id ')[1]

    # Get DB Subnet Group
    dbsgs = sd.get_db_subnet_group(vpcid)
    if not dbsgs:
        print('[*] No DB Subnet Group asociate with Vpc-Id: {}'.format(vpcid))
        dbsgs = sd.create_db_subnet_group(vpcid, engine_version['engine_type'])
    dbsg = cli.ask_for_db_subnet_group(dbsgs)

    # Get available AZ for DB subnet group
    az = sd.get_az_from_db_subnet_group(dbsg['dbsg'])

    # Select license mode
    license_model = cli.ask_for_license_model()

    # Select Instance type
    instance_types = sd.get_instance_types()
    instance_type =cli.ask_for_instance_type(instance_types)

    # Multi AZ
    multi_az = cli.ask_for_multi_az()

    # Public accessible
    public_accesible = cli.ask_for_public_accessible()

    # Charset
    charset = cli.ask_for_charset()

    # Ask for archive_lag_target value
    archive_lag_target = cli.ask_for_archive_lag_target_configuration()

    # Set parameter group name
    parameter_group = '{}-parameter-group'.format(rds_data['rds_instance_name'])

    # Config data
    config_data = {
        'DBName': rds_data['sid'],
        'DBInstanceIdentifier': rds_data['rds_instance_name'],
        'AllocatedStorage': int(storage['storage_size']),
        'DBInstanceClass': instance_type['instance_type'],
        'Engine': engine_version['engine_type'],
        'MasterUsername': rds_data['master_username'],
        'MasterUserPassword': rds_data['master_password'],
        'VpcSecurityGroupIds': sgid,
        'Port': int(rds_data['port']),
        'MultiAZ': bool(multi_az['multi_az']),
        'EngineVersion': minor_version['engine_version'],
        'LicenseModel': license_model['license'],
        'DBParameterGroupName': parameter_group,
        'DBSubnetGroupName': dbsg['dbsg'],
        'AvailabilityZone': az,
        'CharacterSetName': charset['charset'],
        'PubliclyAccessible': bool(public_accesible['public_accessible']),
        'StorageType': storage['storage_type'],
        'StorageEncrypted': storage['storage_encrypte'],
    }

    # Configuration review
    print("""
    ########################
    # Configuration review #
    ########################
    """)
    for key in config_data.keys():
        print('{0:25}  {1}'.format(key, config_data[key]))
    confirmation = cli.ask_for_confirmation()

    if bool(confirmation['confirmation']):
        # Parameter group
        parameter_group_family = sd.get_rds_parameter_group_family(engines, engine_version, minor_version)
        sd.create_rds_parameter_group(parameter_group, rds_data['rds_instance_name'], parameter_group_family)

        # Configure archive_lag_target
        sd.modify_parameter(parameter_group, archive_lag_target)

        # Create instance
        sd.create_rds_instance(config_data)
        sd.rds_instance_is_available()
