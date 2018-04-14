import pytest
import boto3
from moto import mock_dynamodb2
from civil_courage_backend import variables

@pytest.fixture
def event_template():
    return {
        "httpMethod": "",
        "path": "",
        "queryStringParameters": {},
        "body": "",
        "headers": {
            "HOST": "localhost",
            "X_FORWARDED_PROTO": "http"
        }
    }

@pytest.fixture
def dynamodb_service():
    mock_dynamodb2().start()

    dynamodb_resource = boto3.resource("dynamodb")
    dynamodb_client = boto3.client("dynamodb")

    events_table = dynamodb_resource.create_table(
	TableName=variables.events_table_name,
	KeySchema=[
	    {
		'AttributeName': 'id',
		'KeyType': 'HASH'  #Partition key
	    }
	],
	AttributeDefinitions=[
	    {
		'AttributeName': 'id',
		'AttributeType': 'N'
	    }
	],
	ProvisionedThroughput={
	    'ReadCapacityUnits': 5,
	    'WriteCapacityUnits': 5
	}
    )
    
    scenarios_table = dynamodb_resource.create_table(
	TableName=variables.scenarios_table_name,
	KeySchema=[
	    {
		'AttributeName': 'id',
		'KeyType': 'HASH'  #Partition key
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

    events_table.meta.client.get_waiter('table_exists').wait(TableName=variables.events_table_name)
    scenarios_table.meta.client.get_waiter('table_exists').wait(TableName=variables.scenarios_table_name)

    yield (dynamodb_resource, dynamodb_client)

    mock_dynamodb2().stop()
