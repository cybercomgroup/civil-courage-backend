import pytest

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
