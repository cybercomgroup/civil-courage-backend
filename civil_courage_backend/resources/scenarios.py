import boto3
import simplejson as json
from flask import Blueprint, request
from civil_courage_backend import variables

scenarios = Blueprint("scenarios", __name__)

@scenarios.route("/scenarios", methods=["POST"])
def create():
    body = request.get_json(force=True)
    scenarios_table = boto3.resource("dynamodb").Table(variables.scenarios_table_name)
    scenarios_table.put_item(Item=body)
    return ("", 200)

@scenarios.route("/scenarios", methods=["GET"])
def list():
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(variables.scenarios_table_name)
    
    try:
        items = table.scan()["Items"]
    except KeyError:
        items = []

    return (json.dumps(items), 200)

