import pytest
import simplejson as json
from civil_courage_backend import main

@pytest.fixture
def scenarios():
    return [{"id": 1, "hello": "world"}]

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
    items = json.loads(result["body"])
    assert len(items) == 1
    assert items[0] == scenarios[0]


    
