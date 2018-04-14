import pytest
import simplejson as json
from decimal import *
from civil_courage_backend import main, variables

def test_scenario_crud_methods(event_template, dynamodb_service, scenarios):
    (dynamodb_resource, dynamodb_client) = dynamodb_service
    
    event_template["path"] = "/scenarios"
    event_template["httpMethod"] = "POST"
    event_template["body"] = json.dumps(scenarios[0])
    result = main.lambda_handler(event_template, None)
    assert result["statusCode"] == "200"

    event_template["httpMethod"] = "GET"
    result = main.lambda_handler(event_template, None)
    assert result["statusCode"] == "200"
    items = json.loads(result["body"], use_decimal=True)
    assert len(items) == 1
    scenarios[0]["id"] = items[0]["id"]
    assert items[0] == scenarios[0]

@pytest.mark.parametrize("limit, expected", [(1, 1), (None, 2)])
def test_list_scenarios_limit(event_template, dynamodb_service, scenarios, limit, expected):
    (dynamodb_resource, dynamodb_client) = dynamodb_service
    
    table = dynamodb_resource.Table(variables.scenarios_table_name)
    with table.batch_writer() as batch:
        for scenario in scenarios:
            batch.put_item(Item=scenario)
 
    event_template["path"] = "/scenarios"
    event_template["httpMethod"] = "GET"
    event_template["queryStringParameters"]["limit"] = limit
    result = main.lambda_handler(event_template, None)
    assert result["statusCode"] == "200"

    items = json.loads(result["body"])
    assert len(items) == expected

@pytest.mark.parametrize("coordinates, expected", [((56.158915, 13.766765), 1), ((57.0, 12.0), 0)])
def test_latest_scenario(event_template, dynamodb_service, scenarios, events, coordinates, expected):
    (dynamodb_resource, dynamodb_client) = dynamodb_service
    
    table = dynamodb_resource.Table(variables.scenarios_table_name)
    with table.batch_writer() as batch:
        for scenario in scenarios:
            batch.put_item(Item=scenario)
    
    table = dynamodb_resource.Table(variables.events_table_name)
    with table.batch_writer() as batch:
        for event in events:
            batch.put_item(Item=event)
    
    event_template["path"] = "/scenarios/latest"
    event_template["httpMethod"] = "GET"
    event_template["queryStringParameters"]["lat"] = coordinates[0]
    event_template["queryStringParameters"]["lon"] = coordinates[1]
    result = main.lambda_handler(event_template, None)
    assert result["statusCode"] == "200"

    items = json.loads(result["body"])
    assert len(items) == expected

