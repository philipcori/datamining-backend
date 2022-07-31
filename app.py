import json

from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
import logging

from generate_matrix import MatrixClusterGenerator

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = '*'
logging.getLogger('flask_cors').level = logging.DEBUG

matrix_generator = MatrixClusterGenerator()

@app.route('/echo', methods = ['GET'])
@cross_origin()
def echo():
    print('endpoint invoked with request:')
    print(request)
    # name = request.json['name']
    name = request.args.get('name')
    msg = 'Hello ' + str(name)
    resp = make_response(msg)
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    # resp.access_control_allow_origin = "*"
    print('returning response:')
    print(resp.headers)
    return resp

@app.route('/getMatrix', methods = ['GET', 'POST'])
@cross_origin()
def generate_doc_matrix():
    if 'file' not in request.files:
        resp = make_response('No file part')
        return resp
    file = request.files['file']

    # check file is json file
    if file.content_type != 'application/json':
        resp = make_response('File type not supported')
        return resp

    # get file content
    file_content = file.read()
    # convert to json
    json_data = json.loads(file_content)

    url = matrix_generator.generate_matrix(json_data)

    resp = make_response(url)
    return resp










