import boto3
import simplejson as json
from flask import Blueprint, request
from civil_courage_backend import variables

events = Blueprint("events", __name__)

@events.route("/events", methods=["POST"])
def create():
    body = request.get_json(force=True)
    scenarios_table = boto3.resource("dynamodb").Table(variables.events_table_name)
    scenarios_table.put_item(Item=body)
    return ("", 200)

@events.route("/events", methods=["GET"])
def list():
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(variables.events_table_name)
    events = table.scan()["Items"]
    return (json.dumps(events), "200")
