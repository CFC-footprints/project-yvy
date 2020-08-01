from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
from libs.controller_crop import *
from libs.controller_eto import *
from libs.controller_etc import *
from flask_cors import CORS
import atexit
import os
import json

app = Flask(__name__, static_url_path='')
CORS(app)
port = int(os.getenv('PORT', 8000))

#@app.route('/crop_development_stages')
###def crop_development_stages():
#https://getstartedpython-agile-bat-wb.mybluemix.net/etc
@app.route('/crops', methods=['GET'])
def get_grops():
    res = get_cat_name()
    return jsonify(res)

@app.route('/eto', methods=['POST'])
def post_eto():
    req = request.json
    res = get_eto(req["lat"], req["lon"], req["start"], req["end"])
    res = {
        "eto": res
    }
    #return out
    return (res)

@app.route('/etc', methods=['POST'])
def post_etc():
    req = request.json
    res = etc(req)
    #res = {
    #    "etc": res
    #}
    tons = req["tons"]
    hec = req["hectares"]
    prop = float(tons)/float(hec)
    print (prop)
    out = HH(res, prop)
    response = {
        "HH": int(out)
    }
    return (response)

'''
@app.route('/api/visitors', methods=['POST'])
def put_visitor():
    user = request.json['name']
    data = {'name':user}
    if client:
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)
'''

'''
@app.route('/')
def root():
    return app.send_static_file('index.html')

# /* Endpoint to greet and add a new visitor to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Bob"
# * }
# */
@app.route('/api/visitors', methods=['GET'])
def get_visitor():
    if client:
        return jsonify(list(map(lambda doc: doc['name'], db)))
    else:
        print('No database')
        return jsonify([])

# /**
#  * Endpoint to get a JSON array of all the visitors in the database
#  * REST API example:
#  * <code>
#  * GET http://localhost:8000/api/visitors
#  * </code>
#  *
#  * Response:
#  * [ "Bob", "Jane" ]
#  * @return An array of all the visitor names
#  */
@app.route('/api/visitors', methods=['POST'])
def put_visitor():
    user = request.json['name']
    data = {'name':user}
    if client:
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
