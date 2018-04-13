import pytest
import boto3
from moto import mock_dynamodb2

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
    return [{"id":37919,"datetime":"2018-04-13 9:58:49 +02:00","name":"13 april 09.58, Trafikolycka, personskada, Härryda","summary":"På riksväg 40 vid Landvettermotet är det två bilister som kolliderar in i riktning mot Göteborg.","url":"https://polisen.se/aktuellt/handelser/2018/april/13/13-april-09.58-trafikolycka-personskada-harryda/","type":"Trafikolycka, personskada","location":{"name":"Härryda","gps":"57.691744,12.294416"}},{"id":37918,"datetime":"2018-04-13 9:56:41 +02:00","name":"13 april 09.56, Trafikbrott, Gävle","summary":"En man i 50-års åldern rapporteras för grov olovlig körning vid framförande av en moped.","url":"https://polisen.se/aktuellt/handelser/2018/april/13/13-april-10.53-trafikbrott-gavle/","type":"Trafikbrott","location":{"name":"Gävle","gps":"60.67488,17.141273"}}] 

EVENTS_TABLE_NAME="events"

@pytest.fixture
def dynamodb_service(events):
    mock_dynamodb2().start()

    dynamodb_resource = boto3.resource("dynamodb")
    dynamodb_client = boto3.client("dynamodb")

    table = dynamodb_resource.create_table(
	TableName=EVENTS_TABLE_NAME,
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

    table.meta.client.get_waiter('table_exists').wait(TableName=EVENTS_TABLE_NAME)

    with table.batch_writer() as batch:
        for event in events:
            batch.put_item(Item=event)
    
    yield (dynamodb_resource, dynamodb_client)

    mock_dynamodb2().stop()
