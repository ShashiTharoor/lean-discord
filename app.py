import sys,requests,json,os
from datetime import datetime

import leancloud
from flask import Flask, jsonify, request
from flask import render_template
from flask_sockets import Sockets
from leancloud import LeanCloudError
from pytube import YouTube
# from urlparse import urlparse
# from os.path import splitext
app = Flask(__name__)

@app.route('/')
def index():
  return "hello"
  

@app.route('/yt')
def ytupload():
    url=request.args.get('url')
    channel=request.args.get('channel')
    content=request.args.get('content',"")
    auth=request.args.get('auth')
    path = url.split("/")[-1]
    # Split the path into filename and extension
    filename, file_extension = path.split(".", 1) if "." in path else (path, None)
    file_name=request.args.get('filename')
    if file_name==None:
      file_name=path
    else:
      file_name=request.args.get('filename')+"."+file_extension
#     return file_name
    # with open(file_name, 'rb') as f:
    yt = YouTube(url)
    print("downloading Youtube Video")
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(filename=filename, output_path="./")
    ninwo=auth
    header = {'authorization': ninwo}
    payload={'content':content}
    r = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages?limit=10", 
        data=payload, 
        headers=header,
        files={'file': open(f'/tmp/{file_name}', 'rb')}
    )
    return json.dumps(r.json())

    
@app.route('/upload')
def upload():
    url=request.args.get('url')
    channel=request.args.get('channel')
    content=request.args.get('content',"")
    auth=request.args.get('auth')
    path = url.split("/")[-1]
    # Split the path into filename and extension
    filename, file_extension = path.split(".", 1) if "." in path else (path, None)
    file_name=request.args.get('filename')
    if file_name==None:
      file_name=path
    else:
      file_name=request.args.get('filename')+"."+file_extension
#     return file_name
    # with open(file_name, 'rb') as f:
    with requests.get(url, stream=True) as r:
        
        if r.status_code==200:
          r.raise_for_status()
          with open(f'/tmp/{file_name}','wb') as f:
              for chunk in r.iter_content(chunk_size=8192): 
                  f.write(chunk)
        else:
          return f"got 404 not found for {url}"
    # with open(f'/tmp/{file_name}','wb') as file:
    #     file.write(requests.get(url).content)
    ninwo=auth
    header = {'authorization': ninwo}
    payload={'content':content}
    r = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages?limit=10", 
        data=payload, 
        headers=header,
        files={'file': open(f'/tmp/{file_name}', 'rb')}
    )
    return json.dumps(r.json())

@app.route('/upload2')
def uplossad():
    url=request.args.get('url')
    channel=request.args.get('channel')
    content=request.args.get('content',"")
    auth=request.args.get('auth')
    file_name=url.split("/")[-1]
    # with open(file_name, 'rb') as f:
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(f'/tmp/{file_name}','wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    # with open(f'/tmp/{file_name}','wb') as file:
    #     file.write(requests.get(url).content)
    ninwo=auth
    header = {'authorization': ninwo}
    payload={'content':content}
    r = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages?limit=10", 
        data=payload, 
        headers=header,
        files={'file': open(f'/tmp/{file_name}', 'rb')}
    )
    return json.dumps(r.json())

@app.route('/uploads')
def uploads():
    data = request.json # Get the JSON data from the request
    urls = data['urls'] # Extract the URLs from the JSON data
    channel = data['channel']
    content=data.get('content')
    auth=data.get('auth')
    resp=[]
    for url in urls:
      file_name=url.split("/")[-1]
      with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(f'/tmp/{file_name}','wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
      ninwo=auth
      header = {'authorization': ninwo}
      payload={'content':content}
      r = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages?limit=10", 
          data=payload, 
          headers=header,
          files={'file': open(f'/tmp/{file_name}', 'rb')}
      )
      resp.append(r.json())
    return json.dumps(resp)

  
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
