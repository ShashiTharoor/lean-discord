import sys,requests,json,os
from datetime import datetime

import leancloud
from flask import Flask, jsonify, request
from flask import render_template
from flask_sockets import Sockets
from leancloud import LeanCloudError

app = Flask(__name__)

@app.route('/')
def index():
  return "hello"
  
@app.route('/upload')
def upload():
    url=request.args.get('url')
    channel=request.args.get('channel')
    content=request.args.get('content',"")
    file_name=url.split("/")[-1]
    with open(f'/tmp/{file_name}','wb') as file:
        file.write(requests.get(url).content)
    ninwo="MTA5MjQ2MjUzODc5ODY3ODE0Ng.GmlM5O.f8Q4aQRr6qPapoqwe584r-bLW5bwI4Nb6al8RY"
    header = {'authorization': ninwo}
    payload={'content':content}
    r = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages?limit=10", 
        data=payload, 
        headers=header,
        files={'file': open(f'/tmp/{file_name}', 'rb')}
    )
    return json.dumps(r.json())

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

 
# if __name__ == '__main__':
#   app.run(debug=True, port=os.getenv("PORT", default=5001))
