import unittest
from boto3 import resource, client
from moto import mock_dynamodb
from updateCounterInDB import LambdaDynamoDBClass
from updateCounterInDB import lambda_handler, incrementCount


@mock_dynamodb
class TestLambdaHandler(unittest.TestCase):
    def setUp(self):
        # [2] Mock environment & override resources
        self.test_ddb_table_name = "visitCount"

        # [3a] Set up the services: construct a (mocked!) DynamoDB table
        dynamodb = resource("dynamodb") #, region_name="eu-north-1")
        dynamodb.create_table(
            TableName=self.test_ddb_table_name,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        # # [4] Establish the "GLOBAL" environment for use in tests.
        mocked_dynamodb_resource = { "resource" : resource('dynamodb'),
                                     "table_name" : self.test_ddb_table_name  }
        self.mocked_dynamodb_class = LambdaDynamoDBClass(mocked_dynamodb_resource)


    def tearDown(self):
        self.mocked_dynamodb_class.table.delete()


    def test_lambda_handler(self):
        self.mocked_dynamodb_class.table.put_item(
            Item={
                'id': '0',
                'visitCount': 56
            }
        )

        # Call the lambda function
        response = incrementCount(self.mocked_dynamodb_class)

        # Check the response
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], 57)

        # Check the item in the table
        item = self.mocked_dynamodb_class.table.get_item(
            Key={
                'id': '0'
            }
        )['Item']
        self.assertEqual(item['visitCount'], 57)


    def test_lambda_handler_item_not_found(self):
        # Call the lambda function
        response = incrementCount(self.mocked_dynamodb_class)

        # Check the response
        self.assertEqual(response['statusCode'], 404)
        self.assertEqual(response['body'], 'Item not found')


if __name__ == '__main__':
    unittest.main()
