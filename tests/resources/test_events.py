import pytest
import simplejson as json
from civil_courage_backend import main

def test_events_list(event_template, dynamodb_service, events):
    (dynamodb_resource, dynamodb_client) = dynamodb_service

    event_template["path"] = "/events"
    event_template["httpMethod"] = "GET" 
    result = main.lambda_handler(event_template, None)
    assert result["statusCode"] == "200"
    assert result["body"] == json.dumps(events)
