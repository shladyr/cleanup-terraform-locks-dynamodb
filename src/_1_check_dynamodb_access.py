import boto3
import logging

class DynamoDBChecker:
    def __init__(self, aws_access_key, aws_secret_key, aws_region='us-west-2'):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.aws_region = aws_region
        self.dynamodb_client = self._create_dynamodb_client()

    def _create_dynamodb_client(self):
        try:
            session = boto3.Session(
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.aws_region
            )
            return session.client('dynamodb')
        except Exception as e:
            logging.error(f"Failed to create DynamoDB client: {e}")
            raise

    def check_authentication(self):
        try:
            self.dynamodb_client.list_tables()
            logging.info("AWS DynamoDB authentication is successful")
            return True
        except Exception as e:
            logging.error(f"AWS DynamoDB authentication has failed: {e}")
            return False

    def check_dynamodb_exists(self, table_name):
        try:
            existing_tables = self.dynamodb_client.list_tables()['TableNames']
            if table_name in existing_tables:
                logging.info(f"DynamoDB table '{table_name}' exists")
                return True
            else:
                logging.info(f"DynamoDB table '{table_name}' does not exist")
                return False
        except Exception as e:
            logging.error(f"Error while checking DynamoDB existence: {e}")
            return False
