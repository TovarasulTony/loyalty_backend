import json
from flask_api import app

@app.route("/test")
def test():
    return json.dumps({'name': 'alice',
                       'email': 'alice@outlook.com'})
