from argparse import ArgumentParser

def args_external_parser():
    parser = ArgumentParser(description='AWS DynamoDB Cleaner')

    parser.add_argument('AWS_ACCESS_KEY', help='AWS Access Key')
    parser.add_argument('AWS_SECRET_KEY', help='AWS Secret Key')
    parser.add_argument('component',      help='Component value for LockID')
    parser.add_argument('env',            help='Environment value: dev, stage, pre-prod, prod')
    parser.add_argument('webex_token',    help='Webex Teams API token')
    parser.add_argument('room_id',        help='Webex Teams Room ID')
    parser.add_argument('sendwebex',      help='Send to Webex: no, yes')

    return parser
