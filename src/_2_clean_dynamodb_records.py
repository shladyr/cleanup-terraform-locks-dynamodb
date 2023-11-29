import logging
import os

class DynamoDBCleaner:
    def __init__(self, dynamodb_client):
        self.dynamodb_client = dynamodb_client

    def fetch_records(self, table_name, component, env):
        """
        Fetch records from DynamoDB table using Scan operation with provided Filter criteria.
        """
        try:
            response = self.dynamodb_client.scan(
                TableName=table_name,
                FilterExpression='contains(LockID, :pattern)',
                ExpressionAttributeValues={
                    ':pattern': {'S': f'terraform-kubernetes-{component}-{env}'}
                }
            )
            return response['Items']
        except Exception as e:
            logging.error(f"Error while fetching DynamoDB records: {e}")
            return []

    def save_fetched_records_to_file(self, records):
        """
        Save the fetched records to a text file.
        """
        try:
            with open('./fetched-tf-records.txt', 'w') as file:
                for record in records:
                    file.write(str(record) + '\n')
            logging.info("Fetched records saved to fetched-tf-records.txt")
        except Exception as e:
            logging.error(f"Error while saving records to file: {e}")

    def delete_fetched_records(self, table_name, fetched_records):
        """
        Deletes fetched records from the DynamoDB table.
        """
        deleted_records = []
        try:
            for record in fetched_records:
                self.dynamodb_client.delete_item(
                    TableName=table_name,
                    Key={
                        'LockID': {'S': record['LockID']['S']},
                        # Include additional primary key attributes if needed
                    }
                )
                deleted_records.append(record)
            logging.info("Fetched records deleted from DynamoDB table")
        except Exception as e:
            logging.error(f"Error while deleting records: {e}")
        return deleted_records

    def save_deleted_records_to_file(self, deleted_records):
        """
        Save the list of deleted records to a text file.
        """
        file_path = './deleted-tf-records.txt'

        try:
            # Check if the file already exists
            if os.path.exists(file_path):
                logging.warning(f"The file {file_path} already exists and will be overwritten.")

            # Open the file in write mode ('w')
            with open(file_path, 'w') as file:
                # Iterate through each record in the list
                for record in deleted_records:
                    # Write the string representation of the record to the file
                    file.write(str(record) + '\n')

            # Log a message indicating successful save
            logging.info("Deleted records saved to deleted-tf-records.txt")

        except Exception as e:
            # Log an error message if an exception occurs during the file-saving process
            logging.error(f"Error while saving deleted records to file: {e}")
