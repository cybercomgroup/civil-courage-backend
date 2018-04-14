import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import *
import simplejson as json
from flask import Blueprint, request
import urllib.request
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

@events.route("/events/<id>")
def get(id):
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(variables.events_table_name)
    item = table.get_item(Key={"id": int(id)})["Item"]
    return (json.dumps(item), 200) 

@events.route("/events/import", methods=["POST"])
def import_events():
    police_url = "https://polisen.se/H4S-2018-handelser.json"
    ListOfEvents = []

    with urllib.request.urlopen(police_url) as url:
        data = json.loads(url.read().decode('utf-8-sig'))
        for elem in data:
            event = {};
            # create event from elem
            event['id'] = elem['id']
            event['date'] = elem['datetime']
            event['type'] = elem['type']
            gps = elem['location']
            gps = gps['gps']
            gpslist = gps.split(",")
            event['longitude'] = Decimal(gpslist[1])
            event['latitude'] = Decimal(gpslist[0])
            event['id'] = elem['id']
            name = elem['name']
            nameparts = name.split(",")
            place = nameparts[len(nameparts) - 1]
            place = place[1:]
            event['place'] = place
            event['name'] = elem['type'] + " i " + place
            ListOfEvents.append(event)
 
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(variables.events_table_name)
    with table.batch_writer() as batch:
        for event in ListOfEvents:
            batch.put_item(Item=event)

    return ("", 200)
