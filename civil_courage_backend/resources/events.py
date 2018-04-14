import boto3
import simplejson as json
from flask import Blueprint, request
from civil_courage_backend import variables

events = Blueprint("events", __name__)

@events.route("/events", methods=["POST"])
def create():
    body = json.loads(request.data, use_decimal=True)
    scenarios_table = boto3.resource("dynamodb").Table(variables.events_table_name)
    scenarios_table.put_item(Item=body)
    return ("", 200)

@events.route("/events", methods=["GET"])
def list():
    limit = request.args.get("limit", default=None, type=int)
    
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(variables.events_table_name)
    
    if limit:
        items = table.scan(Limit=limit).get("Items", [])
    else:
        items = table.scan().get("Items", [])
    
    return (json.dumps(items), "200")
