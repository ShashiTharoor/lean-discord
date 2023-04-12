import sys,requests
from datetime import datetime

import leancloud
from flask import Flask, jsonify, request
from flask import render_template
from flask_sockets import Sockets
from leancloud import LeanCloudError

from views.todos import todos_view
app = Flask(__name__)

@app.route('/')
def index():
  return "hello"
  
@app.route('/upload')
def upload():


@app.route('/time')
def time():
    return str(datetime.now())


@app.route('/version')
def print_version():
    import sys
    return sys.version
  
@app.route('/api/python-version', methods=['GET'])
def python_version():
    return jsonify({"python-version": sys.version})

 
 if __name__ == '__main__':
  app.run(debug=True, port=os.getenv("PORT", default=5001))