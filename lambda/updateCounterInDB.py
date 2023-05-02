import boto3
import json

# Set up the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = 'visitCount'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    response = table.get_item(
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
    response = table.update_item(
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
