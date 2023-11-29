
# CleanUp Terraform Locks in Aws DynamoDB
This Python script fetches and deletes terraform locks stored in Aws DynamoDB Table "terraform-locks".

## Overview
The script is designed to:

- Verify authentication to AWS DynamoDB.
- Check for the existence of a specified Aws DynamoDB table.
- Fetch and save records based on specific criteria.
- Delete fetched records from the DynamoDB table.

## Requirements
Python 3.6 or higher
Boto3 Library: It is used for interacting with AWS services.
Install Boto3 using pip: (`pip install boto3`)

## Setup
1. Clone or download the script to your local environment.
2. Install Dependencies
Make sure to have Python installed. Install the required Boto3 library:

    ```
    pip install boto3
    ```
3. Run the Script
Execute the Python script (script_name.py) using the following command:

```
python cleanup_terraform_locks.py [AWS_ACCESS_KEY] [AWS_SECRET_KEY] [component] [env]
```
Replace [AWS_ACCESS_KEY], [AWS_SECRET_KEY], [component], and [env] with your AWS credentials, component value for LockID, and environment value (dev, stage, pre-prod, prod) respectively.

## Execution
The script uses the provided AWS credentials to authenticate with AWS DynamoDB. 
It checks for the specified DynamoDB table, fetches records based on given criteria, saves fetched records to a text file, and deletes the fetched records from the DynamoDB table.

## Command-line Arguments
- AWS_ACCESS_KEY: Your AWS Access Key.
- AWS_SECRET_KEY: Your AWS Secret Key.
- component: Component value for LockID.
- env: Environment value (dev, stage, pre-prod, prod).

## Jenkins Credentials
The Aws Secrets are stored in the Jenkins Credentials:
- Stage: https://jenkins-ares.cdaas.umbrella.com/manage/credentials/store/system/domain/_/credential/jenkins-to-aws-stage-dynamodb-terraform-locks/
- Prod: https://jenkins-ares.cdaas.umbrella.com/manage/credentials/store/system/domain/_/credential/jenkins-to-aws-prod-dynamodb-terraform-locks/

## Webex Credentials
Room ID: https://jenkins-ares.cdaas.umbrella.com/manage/credentials/store/system/domain/_/credential/MARS_NOTIFY_ROOM_ID/
Bot token: https://jenkins-ares.cdaas.umbrella.com/manage/credentials/store/system/domain/_/credential/webex-teams-mars-bot-access-token/

## QA Webex Credentials
```
     [$class: 'StringBinding', credentialsId: 'SERHII_WEBEX_TOKEN', variable: 'TEST_WEBEX_TOKEN'],
     [$class: 'StringBinding', credentialsId: 'SERHII_ROOM_ID', variable: 'TEST_ROOM_ID'],
     
     python3 modules/cleanup_terraform_locks/main.py ${AWS_ACCESS_KEY_ID} ${AWS_SECRET_ACCESS_KEY} ${component} ${env} ${TEST_WEBEX_TOKEN} ${TEST_ROOM_ID} ${action}
```

## Prod Webex Credentials
https://jenkins-ares.cdaas.umbrella.com/manage/credentials/store/system/domain/_/credential/webex-teams-mars-bot-access-token/
```
        credentials(
            name: 'WEBEX_TEAMS_CREDENTIALS', 
            description: 'Webex Teams Bot credentials ID',
            defaultValue: 'webex-teams-mars-bot-access-token',
            credentialType: "Username with password", 
            required: true 
        )
        string(
            name: 'SPACE_ID',
            defaultValue: 'Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hOmlkZW50aXR5TG9va3VwL1JPT00vNzMxZjQ0MTAtZDQxNi0xMWViLWI3YWYtYzk2OGJlNDY1YzA0', // spaceName: 'Mars Notifications'
            description: 'The space ID of the webex teams room to notify'
        )
```
OR
```angular2html
     [$class: 'StringBinding', credentialsId: 'webex-teams-mars-bot-access-token', variable: 'MARS_NOTIFY_WEBEX_TOKEN'],
     [$class: 'StringBinding', credentialsId: 'MARS_NOTIFY_ROOM_ID', variable: 'MARS_NOTIFY_ROOM_ID'],
```

## Script Output
The script provides the following output:

Authentication status for AWS DynamoDB.
Existence check for the specified DynamoDB table.
Fetched records based on provided criteria.
List of deleted records.
Saving records to text files.

## Important Note
- Ensure proper configurations and permissions are set for AWS access to DynamoDB tables.
- Take caution when deleting records from the DynamoDB table, as the process is irreversible.

## Links
- JOB: https://jenkins-ares.cdaas.umbrella.com/job/ares.jobs/job/tool.cleanup.terraform.locks.deynamodb/
- RUNBOOK: https://confluence-eng-rtp2.cisco.com/conf/pages/viewpage.action?pageId=472581487
- AWS IAM: https://us-east-1.console.aws.amazon.com/iam/home?region=us-west-2#/users/details/jenkins-cleanup-terraform-locks
- AWS IAM Policy: inside IAM user
- AWS IAM Role: N/A