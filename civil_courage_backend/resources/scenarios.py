import math
from random import randint
import boto3
import simplejson as json
from flask import Blueprint, request
from civil_courage_backend import variables

scenarios = Blueprint("scenarios", __name__)

@scenarios.route("/scenarios", methods=["POST"])
def create():
    body = json.loads(request.data, use_decimal=True)
    body["id"] = "{}-{}".format(body["event_id"], randint(10, 99))
    scenarios_table = boto3.resource("dynamodb").Table(variables.scenarios_table_name)
    scenarios_table.put_item(Item=body)
    return ("", 200)

@scenarios.route("/scenarios", methods=["GET"])
def list():
    limit = request.args.get("limit", default=None, type=int)
    
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(variables.scenarios_table_name)

    if limit:
        items = table.scan(Limit=limit).get("Items", [])
    else:
        items = table.scan().get("Items", [])

    return (json.dumps(items), 200)

@scenarios.route("/scenarios/latest", methods=["GET"])
def latest():
    lon1 = request.args.get("lon", type=float)
    lat1 = request.args.get("lat", type=float)
    radius = request.args.get("radius", default=20, type=float)
    
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(variables.scenarios_table_name)

    # Iterate through items and check radius
    items = table.scan()["Items"]
    result = []
    for item in items:
        lat2, lon2 = (float(item["latitude"]), float(item["longitude"]))
        earth_radius = 6371 # km

        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = int(earth_radius * c)
 
        if d <= radius:
            result.append(item)	
    
    return (json.dumps(result), 200)


