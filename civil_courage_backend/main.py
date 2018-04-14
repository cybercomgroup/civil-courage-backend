import awsgi
from flask import Flask

try:
    from resources import events, scenarios, data
except:
    import os, sys
    base = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(base)
    from resources import events, scenarios, data

app = Flask(__name__)
app.register_blueprint(events.events)
app.register_blueprint(scenarios.scenarios)
app.register_blueprint(data.data)

@app.route("/")
def index():
    return ("OK", 200)

def lambda_handler(event, context):
    response = awsgi.response(app, event, context)
    response["isBase64Encoded"] = False
    cors_header = {
        "X-Requested-With": '*',
        "Access-Control-Allow-Headers": 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with',
        "Access-Control-Allow-Origin": '*',
        "Access-Control-Allow-Methods": 'POST,GET,OPTIONS'
    }

    response["headers"] = cors_header
    return response

