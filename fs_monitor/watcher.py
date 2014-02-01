import configparser
import json
import http.client
import os
import sys
import time
import urllib.parse

from watchdog.observers import Observer
import requests

from EventHandler import EventHandler


def list_dir(root, prefix):
    dir = []
    if os.path.isdir(root):
        for entry in os.listdir(root):
            path = os.path.join(root, entry)
            it = {'name': str(os.path.relpath(path, prefix)), 't':'', 'items':'' }
            if os.path.isdir(path):
                 it['t'] = 'dir'
                 it['items'] = list_dir(path, prefix)
            elif os.path.isfile(path):
                 it['t'] = 'file'
            dir.append(it)
    else:
        return {}

    return dir


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    print(config.sections())
    paths = [config['Data']['sync_dir']]
    url = config['Server']['url']
    username = config['Data']['username']
    password = config['Data']['password']


    session = requests.Session()
    session.post(url+"/login",
                 data=("username="+username+"&"+"password="+password)
                 )

    remote_index = session.get(url+"/api/tree").text
    local_index = {"items" : list_dir(config['Data']['sync_dir'], config['Data']['prefix']),
                   "name" : "/",
                   "t" : "dir"
                   }


    print("Remote: \n",json.dumps(eval(remote_index), sort_keys=True,
                     indent=4, separators=(',',':')), "\n\n")

    print("Local: \n",json.dumps(local_index, sort_keys=True,
                     indent=4, separators=(',',':')))


#    paths = [ x for x in sys.argv[1:] ] or '.'
#    paths = sys.argv[1] or '.'
#    print("The paths to be monitored are: ", paths)


    event_handler = EventHandler(session, url, local_index, remote_index)
    to_watch = Observer()

    for path in paths:
        to_watch.schedule(event_handler, path, recursive=True)
    to_watch.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        to_watch.stop()
    to_watch.join()


main()
