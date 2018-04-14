import pytest
from decimal import *
import simplejson as json
from civil_courage_backend import main, variables

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
    items = json.loads(result["body"], use_decimal=True)
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

    items = json.loads(result["body"], use_decimal=True)
    assert len(items) == expected

def test_get_event(event_template, dynamodb_service, events):
    (dynamodb_resource, dynamodb_client) = dynamodb_service
    
    table = dynamodb_resource.Table(variables.events_table_name)
    table.put_item(Item=events[0])
 
    event_template["path"] = "/events/{}".format(events[0]["id"])
    event_template["httpMethod"] = "GET"
    result = main.lambda_handler(event_template, None)
    assert result["statusCode"] == "200"

    item = json.loads(result["body"], use_decimal=True)
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

    items = json.loads(result["body"], use_decimal=True)
    assert len(items) == 500

    
