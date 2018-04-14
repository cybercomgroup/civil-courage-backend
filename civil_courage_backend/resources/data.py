import boto3
import simplejson as json
from flask import Blueprint, request

data = Blueprint("data", __name__)

@data.route("/data/import")
def import_data():
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table("events")
    return ("OK", "200")
