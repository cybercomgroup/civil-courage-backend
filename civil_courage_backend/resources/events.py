import boto3
import simplejson as json
from flask import Blueprint, request

events = Blueprint("events", __name__)

@events.route("/events")
def list():
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table("events")
    events = table.scan()["Items"]
    print(events)
    return (json.dumps(events), "200")
