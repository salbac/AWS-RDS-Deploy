# AWS RDS Deploy Tool
With this tool you can deploy new RDS instance in your AWS account.

Runed in interactive mode doing questions to the user and guide him for complete the process.

## Limitations
At this moment only support Oracle engine

## Script setup
The tool was developed using Python 3.7.6 in OSX.

This script is based in two non-standard Python libraries.

* [PyInquirer](https://github.com/CITGuru/PyInquirer)
* [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

Download this repository from commandline:
````shell script
wget https://github.com/salbac/AWS-RDS-Deploy/archive/master.zip
````
Unzip file:
```shell script
unzip master.zip
```

Install requirements.
````shell script
cd AWS_RDS_Deploy_master
pip install -r requirements.txt
````

## AWS Permisions
The IAM user need the following permisions:
* **AmazonRDSFullAccess** 
* **AmazonEC2ReadOnlyAccess** 

Possibly the permissions could be limited more, but these were the permissions with which the script was developed. In the future they will be reviewed.

## How to use
In the command line inside the downloaded folder execute:
```shell script
python3 aws_rds_deploy.py
```
And response all questions prompted by the wizard.

## TODOs
* Unit Tests
* Configure backups in instance
* Configure Performance Insights
* Unlock all engines
* Restrict acces with Security Group


