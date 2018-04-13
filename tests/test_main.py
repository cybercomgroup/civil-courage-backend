import pytest
from civil_courage_backend import main

def test_lambda_handler_existing_method(event_template):
    event_template["path"] = "/"
    event_template["httpMethod"] = "GET" 
    result = main.lambda_handler(event_template, None)
    assert result["statusCode"] == "200"
    assert result["body"] == "OK"

def test_lambda_handler_non_existing_method(event_template):
    event_template["path"] = "/missing-path"
    event_template["httpMethod"] = "GET" 
    result = main.lambda_handler(event_template, None)
    assert result["statusCode"] == "404"
