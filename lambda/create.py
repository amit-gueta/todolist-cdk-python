import json
import os
import logging
import jwt
import uuid
import boto3

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)


def main(event, context):
    LOG.info("EVENT: " + json.dumps(event))
    # Pull out the DynamoDB table name from environment
    table_name = os.environ.get('TABLE_NAME')

    if (not event['body']):
        return {
            'statusCode': 400,
            'body': "invalid request, you are missing the parameter body"
        }
    ddict = {
        'id': 7,
        'known': False,
        'score': 0,
        'translated': "מעבר ל; מקצה לקצה של",
        'unit': 1,
        'word': "accros"
    }
    item = json.loads(event['body'])
    auth = jwt.decode(event['headers']["Authorization"],
                      options={"verify_signature": False})
    LOG.debug("auth::::: " + json.dumps(auth))
    item["userId"] = auth['sub']
    item["todoId"] = str(uuid.uuid4())
    item["test"] = ddict
    LOG.debug("finish " + json.dumps(item["todoId"]))
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    # Get my table
    table = dynamodb.Table(table_name)

    try:
        response = table.put_item(
            Item=item)
        LOG.debug("RESPONSE: " + json.dumps(response))
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    except Exception as e:
        return {'statusCode': 500,
                'body': str(e)
                }
