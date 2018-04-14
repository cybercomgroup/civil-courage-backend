from decimal import *
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
def events():
    return [{"date": "2018-04-09 13:00:01 +02:00", "place": "H\u00e4ssleholm", "latitude": Decimal("59.341267"), "id": 1, "longitude": Decimal("18.063502"), "name": "R\u00e5n i H\u00e4ssleholm", "type": "R\u00e5n"}, {"date": "2018-04-10 9:54:52 +02:00", "place": "Lycksele", "latitude": Decimal("64.59581"), "id": 4, "longitude": Decimal("18.676367"), "name": "Trafikbrott i Lycksele", "type": "Trafikbrott"}]
 
@pytest.fixture
def scenarios():
    return [{"id": "1-20", "event_id": 1, "append_text": "test test", "severity": 2, "type": 0}, {"id": "4-20", "event_id": 4, "type": 1, "severity": 2, "append_text": "hello world"}]

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
