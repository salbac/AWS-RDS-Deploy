# AWS-RDS-Deploy
The following script is designed for ask the necessary questions to the user for automating deploy new RDS instance in selected AWS account.

At this moment only support Oracle engine

## Script setup
The Python version requested by the script is 3.7.6 and only support the following operatin systems:
* MacOSX
* Linux
* Unix

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
cd AWS-RDS-Deploy-master
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
python3 aws-rds-deploy.py
```
And response all questions prompted by the wizard.

