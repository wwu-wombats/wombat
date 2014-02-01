from bottle import route, request, static_file
import bottle
import os

FILE_ROOT = "/home/kellen/webfs/tmp"

@route('/upload', method='POST')
def do_upload():
    #data =  request.body.read()
    filename = request.json['title']
    filename = ''.join([x for x in filename if x.isalnum() or x == '.'])
    payload = request.json['payload']
    print "Uploaded: " + filename
    with open(os.path.join('./tmp',filename), "w") as f:
        f.write(payload.encode('ascii'))

@route('/')
def index():
    return static_file('index.html', root=".")

@route('/list')
@route('/list/')
@route('/list/<directory>')
def list(directory = None):
    if directory:
        root = os.path.join(FILE_ROOT, directory)
    else:
        root = FILE_ROOT

    items = os.listdir(root)

    json = { 'items': items }

    return json

@route('/donwload/<file>')
@route('/download/<file:path>')
def download(file):
    path = os.path.join(FILE_ROOT, file)
    root, filename = os.path.split(path)
    print filename
    return static_file(filename, root)

@route('/webfs.js')
def js():
    return static_file('webfs.js', root='.')

bottle.run(host='localhost', port=8080)
