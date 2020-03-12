from PyInquirer import prompt

import cli.cli_validators as validator


class Cli(object):

    def ask_for_aws_auth_type(self):
        questions = [
            {
                'type': 'list',
                'message': 'Select AWS auth type',
                'name': 'auth_type',
                'choices': [
                    {
                        'name': 'AWS Key'
                    },
                    {
                        'name': 'AWS Token'
                    }
                ],
                'validate': validator.EmptyValidator
            },
            {
                'type': 'password',
                'message': 'Enter your AWS token',
                'name': 'aws_token',
                'when': lambda answers: answers['auth_type'] == 'AWS Token',
                'validate': validator.EmptyValidator
            },
            {
                'type': 'password',
                'message': 'Enter your AWS acces Key',
                'name': 'aws_access_key',
                'when': lambda answers: answers['auth_type'] == 'AWS Key',
                'validate': validator.EmptyValidator
            },
            {
                'type': 'password',
                'message': 'Enter your AWS secret Key',
                'name': 'aws_secret_key',
                'when': lambda answers: answers['auth_type'] == 'AWS Key',
                'validate': validator.EmptyValidator
            }
        ]
        auth = prompt(questions)
        return auth

    def ask_for_region(self, regions):
        questions = [
            {
                'type': 'list',
                'name': 'region',
                'message': 'Select AWS region:',
                'choices': regions,
                'validate': validator.EmptyValidator
            }
        ]

        answers = prompt(questions)
        return answers['region']

    def ask_for_vpcs(self, vpcs):
        questions = [
            {
                'type': 'list',
                'name': 'vpc',
                'message': 'Select AWS VPC:',
                'choices': vpcs,
                'validate': validator.EmptyValidator
            }
        ]
        answers = prompt(questions)
        return answers

    def ask_for_sg(self, sgs):
        questions = [
            {
                'type': 'list',
                'name': 'sg',
                'message': 'Select AWS security group:',
                'choices': sgs,
                'validate': validator.EmptyValidator
            }
        ]
        answers = prompt(questions)
        return answers

    def ask_for_db_subnet_group(self, dbsg):
        questions = [
            {
                'type': 'list',
                'name': 'dbsg',
                'message': 'Select AWS DB subnet group:',
                'choices': dbsg,
                'validate': validator.EmptyValidator
            }
        ]
        answers = prompt(questions)
        return answers

    def ask_for_rds_instance_name(self):
        questions = [
            {
                'type': 'input',
                'name': 'rds_instance_name',
                'message': 'What name do you want to guive to the RDS instance?',
                'validate': validator.RdsInstanceNameValidator
            }
        ]
        answers = prompt(questions)
        return answers

    def ask_for_rds_data(self):
        questions = [
            {
                'type': 'input',
                'name': 'sid',
                'message': 'What name do you want to guive to SID?',
                'validate': validator.OracleSystemIdValidator,
                'default': 'orcl'
            },
            {
                'type': 'input',
                'name': 'master_username',
                'message': 'What is the master username?',
                'validate': validator.MasterUsernameValidator,
                'default': 'root'
            },
            {
                'type': 'password',
                'name': 'master_password',
                'message': 'What is the master password?',
                'validate': validator.MasterPasswordValidator,
            },
            {
                'type': 'input',
                'name': 'port',
                'message': 'What is the database port?',
                'default': '1521',
                'validate': validator.PortValidator
            },
        ]
        answers = prompt(questions)
        return answers

    def ask_for_archive_lag_target_configuration(self):
        questions = [
            {
                'type': 'list',
                'name': 'archive_lag_target',
                'message': 'Select value for archive_lag_target:',
                'choices': [
                    {
                        'name': '60',
                    },
                    {
                        'name': '120',
                    },
                    {
                        'name': '180',
                    },
                    {
                        'name': '240',
                    },
                    {
                        'name': '300',
                    },
                ],
                'validate': validator.EmptyValidator
            },
        ]
        answers = prompt(questions)
        return answers

    def ask_for_storage(self):
        questions = [
            {
                'type': 'list',
                'name': 'storage_type',
                'message': 'Select storage type:',
                'choices': [
                    {
                        'key': 'storage',
                        'name': 'General Purpose SSD',
                        'value': 'gp2'
                    },
                    {
                        'key': 'storage',
                        'name': 'Provisioned IOPS',
                        'value': 'io1'
                    },
                    {
                        'key': 'storage',
                        'name': 'Magnetic',
                        'value': 'standard'
                    }
                ],
                'validate': validator.EmptyValidator
            },
            {
                'type': 'input',
                'name': 'storage_size',
                'message': 'How muche storage do you want to configure??',
                'default': '20',
                'validate': validator.IntegerValidator
            },
            {
                'type': 'confirm',
                'name': 'storage_encrypte',
                'message': 'Want to encrypt storage?',
                'default': True
            },
        ]
        answers = prompt(questions)
        return answers

    def ask_for_engine(self, engines):
        questions = [
            {
                'type': 'list',
                'name': 'engine_type',
                'message': 'Select engine type:',
                'choices': engines,
                'validate': validator.EmptyValidator
            },
        ]
        answers = prompt(questions)
        return answers

    def ask_for_engine_version(self, engines):
        questions = [
            {
                'type': 'list',
                'name': 'engine_version',
                'message': 'Select engine version:',
                'choices': engines,
                'validate': validator.EmptyValidator
            },
        ]
        answers = prompt(questions)
        return answers

    def ask_for_instance_type(self, instance_types):
        questions = [
            {
                'type': 'list',
                'name': 'instance_type',
                'message': 'Select instance type:',
                'choices': instance_types,
                'validate': validator.EmptyValidator
            },
        ]
        answers = prompt(questions)
        return answers

    def ask_for_license_model(self):
        questions = [
            {
                'type': 'list',
                'name': 'license',
                'message': 'Select engine version:',
                'choices': [
                    {
                        'name': 'bring-your-own-license',
                    },
                    {
                        'name': 'license-included',
                    },
                    {
                        'name': 'general-public-license',
                    }
                ],
                'validate': validator.EmptyValidator
            },
        ]
        answers = prompt(questions)
        return answers

    def ask_for_multi_az(self):
        questions = [
            {
                'type': 'confirm',
                'name': 'multi_az',
                'message': 'Is MultiAZ instance?',
                'default': False
            },
        ]
        answers = prompt(questions)
        return answers

    def ask_for_public_accessible(self):
        questions = [
            {
                'type': 'confirm',
                'name': 'public_accessible',
                'message': 'The instance need public accesibility?',
                'default': False
            },
        ]
        answers = prompt(questions)
        return answers

    def ask_for_charset(self):
        charsets = ['AL32UTF8', 'AR8ISO8859P6', 'AR8MSWIN1256', 'BLT8ISO8859P13', 'BLT8MSWIN1257', 'CL8ISO8859P5', 'CL8MSWIN1251', 'EE8ISO8859P2', 'EL8ISO8859P7', 'EE8MSWIN1250', 'EL8MSWIN1253', 'IW8ISO8859P8', 'IW8MSWIN1255', 'JA16EUC', 'JA16EUCTILDE', 'JA16SJIS', 'JA16SJISTILDE', 'KO16MSWIN949', 'NE8ISO8859P10', 'NEE8ISO8859P4', 'TH8TISASCII', 'TR8MSWIN1254', 'US7ASCII', 'UTF8', 'VN8MSWIN1258', 'WE8ISO8859P1', 'WE8ISO8859P15', 'WE8ISO8859P9', 'WE8MSWIN1252', 'ZHS16GBK', 'ZHT16HKSCS', 'ZHT16MSWIN950', 'ZHT32EUC']
        res = []
        for charset in charsets:
            res.append({'name': charset})
        questions = [
            {
                'type': 'list',
                'name': 'charset',
                'message': 'Select database charset:',
                'choices': res,
                'validate': validator.EmptyValidator
            },
        ]
        answers = prompt(questions)
        return answers

    def ask_for_parameter_group_name(self):
        questions = [
            {
                'type': 'input',
                'name': 'parameter_group_name',
                'message': 'What is the name of new parameter group?',
                'validate': validator.EmptyValidator
            },
        ]
        answers = prompt(questions)
        return answers

    def ask_for_confirmation(self):
        questions = [
            {
                'type': 'confirm',
                'name': 'confirmation',
                'message': 'Do you want to proceed with the installation?',
                'default': True
            },
        ]
        answers = prompt(questions)
        return answers


