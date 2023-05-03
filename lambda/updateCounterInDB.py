import boto3
import json


_LAMBDA_DYNAMODB_RESOURCE = { "resource" : boto3.resource('dynamodb'),
                              "table_name" : 'visitCount' }


class LambdaDynamoDBClass:
    def __init__(self, lambda_dynamodb_resource):
        self.resource = lambda_dynamodb_resource["resource"]
        self.table_name = lambda_dynamodb_resource["table_name"]
        self.table = self.resource.Table(self.table_name)


def lambda_handler(event, context):

    global _LAMBDA_DYNAMODB_RESOURCE

    dynamodb_resource_class = LambdaDynamoDBClass(_LAMBDA_DYNAMODB_RESOURCE)

    return incrementCount(dynamo_db = dynamodb_resource_class)


def incrementCount(dynamo_db):
    response = dynamo_db.table.get_item(
        Key={
            'id': '0'
        }
    )
    
    # Check if the item exists
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': 'Item not found'
        }
        
    newCount = response['Item']['visitCount']+1
    
    # Update the item in the DynamoDB table
    response = dynamo_db.table.update_item(
        Key={
            'id': '0'
        },
        UpdateExpression='SET visitCount = :val1',
        ExpressionAttributeValues={
            ':val1': newCount
        }
    )

    # Return a response object
    return {
        'statusCode': 200,
        'body': newCount,
        'headers': {
            'access-control-allow-origin': "https://lenaan.link/*"
        }
    }
