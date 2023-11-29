#!/usr/local/bin/python3

import logging
from src._1_check_dynamodb_access import DynamoDBChecker
from src._2_clean_dynamodb_records import DynamoDBCleaner
from src._3_send_records_webex import SendToWebexTeams
from src import _0_parse_args_external_file

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def main():
    parser = _0_parse_args_external_file.args_external_parser()
    args = parser.parse_args()
    setup_logging()

    dynamodb_checker = DynamoDBChecker(args.AWS_ACCESS_KEY, args.AWS_SECRET_KEY)
    webex_sender = SendToWebexTeams(args.webex_token, args.room_id, args.sendwebex)

    if dynamodb_checker.check_authentication():
        table_name = "terraform-locks"  # The name of the DynamoDB table to check
        if dynamodb_checker.check_dynamodb_exists(table_name):
            print(f"DynamoDB table '{table_name}' exists.")

            dynamodb_cleaner = DynamoDBCleaner(dynamodb_checker.dynamodb_client)

            # Fetch records based on provided Filter criteria
            fetched_records = dynamodb_cleaner.fetch_records(table_name, args.component, args.env)

            # Send fetched records to Webex Teams
            if fetched_records:
                message = "\n".join([str(record) for record in fetched_records])
                webex_sender.send_to_webex_room(f"Fetched list of terraform locks for {args.component} in EKS {args.env}:\n{message}", args.sendwebex)
            else:
                webex_sender.send_to_webex_room(f"No any terraform locks in Aws DynamoDB for {args.component} in EKS {args.env}", args.sendwebex)

            # Print fetched records
            if fetched_records:
                print("Fetched Records:")
                for record in fetched_records:
                    print(record)
            else:
                print("No records found with the given criteria.")

            # Save fetched records to a text file
            dynamodb_cleaner.save_fetched_records_to_file(fetched_records)

            # Delete fetched records
            deleted_records = dynamodb_cleaner.delete_fetched_records(table_name, fetched_records)

            # Print list of deleted records
            if deleted_records:
                print("Deleted Records:")
                for record in deleted_records:
                    print(record)
                dynamodb_cleaner.save_deleted_records_to_file(deleted_records)
            else:
                print("No records deleted.")
        else:
            print(f"DynamoDB table '{table_name}' does not exist.")
    else:
        print("AWS DynamoDB authentication has failed.")

if __name__ == "__main__":
    main()
