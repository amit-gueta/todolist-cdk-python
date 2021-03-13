import json
import os
import logging
import jwt
import uuid
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def main(event, context):
    LOG.info("EVENT: " + json.dumps(event))
    # Pull out the DynamoDB table name from environment
    table_name = os.environ.get('TABLE_NAME')

    auth = jwt.decode(event['headers']["Authorization"],
                      options={"verify_signature": False})

    userId = auth['sub']
    if (not userId):
        return {
            'statusCode': 400,
            'body': "invalid request, you are missing the parameter body"
        }

    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    # Get my table
    table = dynamodb.Table(table_name)
    LOG.debug("RESPONSE: " + json.dumps(userId))
    try:
        response = table.query(
            KeyConditionExpression=Key('userId').eq(userId)
        )
        #LOG.debug("RESPONSE: " + json.dumps(response))
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'], indent=4, cls=DecimalEncoder)
        }
    except Exception as e:
        return {'statusCode': 500,
                'body': str(e)
                }
