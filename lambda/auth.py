import json
import os
import logging

import boto3

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)


def main(event, context):
    LOG.info(f"EVENT:  {json.dumps(event)}")
    # Pull out the DynamoDB table name from environment
    table_name = os.environ.get('TABLE_NAME')

    if (not event['body']):
        return {
            'statusCode': 400,
            'body': "invalid request, you are missing the parameter body"
        }

    body = json.loads(event['body'])

    cognito = boto3.client('cognito-idp')
    try:
        response = cognito.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': body["email"],
                'PASSWORD': body["password"]
            },
            ClientId=event['headers']["client-id"])
        LOG.debug(f"RESPONSE: {json.dumps(response)}")
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent,client-id'
            },
            'body': json.dumps(response)
        }
    except Exception as e:
        return {'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent,client-id'
                },
                'body': str(e)
                }
