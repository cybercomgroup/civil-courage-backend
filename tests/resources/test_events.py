import pytest
import simplejson as json
from civil_courage_backend import main, variables

@pytest.fixture
def events():
    return [{"id":37919,"datetime":"2018-04-13 9:58:49 +02:00","name":"13 april 09.58, Trafikolycka, personskada, Härryda","summary":"På riksväg 40 vid Landvettermotet är det två bilister som kolliderar in i riktning mot Göteborg.","url":"https://polisen.se/aktuellt/handelser/2018/april/13/13-april-09.58-trafikolycka-personskada-harryda/","type":"Trafikolycka, personskada","location":{"name":"Härryda","gps":"57.691744,12.294416"}},{"id":37918,"datetime":"2018-04-13 9:56:41 +02:00","name":"13 april 09.56, Trafikbrott, Gävle","summary":"En man i 50-års åldern rapporteras för grov olovlig körning vid framförande av en moped.","url":"https://polisen.se/aktuellt/handelser/2018/april/13/13-april-10.53-trafikbrott-gavle/","type":"Trafikbrott","location":{"name":"Gävle","gps":"60.67488,17.141273"}}] 

def test_events_crud(event_template, dynamodb_service, events):
    (dynamodb_resource, dynamodb_client) = dynamodb_service
    
    event_template["path"] = "/events"
    event_template["httpMethod"] = "POST"
    event_template["body"] = json.dumps(events[0])
    result = main.lambda_handler(event_template, None)
    assert result["statusCode"] == "200"

    event_template["httpMethod"] = "GET" 
    result = main.lambda_handler(event_template, None)
    assert result["statusCode"] == "200"
    items = json.loads(result["body"])
    assert len(items) == 1
    assert items[0] == events[0]

@pytest.mark.parametrize("limit, expected", [(1, 1), (None, 2)])
def test_list_events_limit(event_template, dynamodb_service, events, limit, expected):
    (dynamodb_resource, dynamodb_client) = dynamodb_service
    
    table = dynamodb_resource.Table(variables.events_table_name)
    with table.batch_writer() as batch:
        for event in events:
            batch.put_item(Item=event)
 
    event_template["path"] = "/events"
    event_template["httpMethod"] = "GET"
    event_template["queryStringParameters"]["limit"] = limit
    result = main.lambda_handler(event_template, None)
    assert result["statusCode"] == "200"

    items = json.loads(result["body"])
    assert len(items) == expected

def test_get_event(event_template, dynamodb_service, events):
    (dynamodb_resource, dynamodb_client) = dynamodb_service
    
    table = dynamodb_resource.Table(variables.events_table_name)
    table.put_item(Item=events[0])
 
    event_template["path"] = "/events/{}".format(events[0]["id"])
    event_template["httpMethod"] = "GET"
    result = main.lambda_handler(event_template, None)
    assert result["statusCode"] == "200"

    item = json.loads(result["body"])
    assert item == events[0]

def test_events_import(event_template, dynamodb_service):
    (dynamodb_resource, dynamodb_client) = dynamodb_service
     
    event_template["path"] = "/events/import"
    event_template["httpMethod"] = "POST"
    result = main.lambda_handler(event_template, None)
    assert result["statusCode"] == "200"
    
    event_template["path"] = "/events"
    event_template["httpMethod"] = "GET"
    result = main.lambda_handler(event_template, None)
    assert result["statusCode"] == "200"

    items = json.loads(result["body"])
    assert len(items) == 500

    
