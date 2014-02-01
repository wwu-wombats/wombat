import json
import http.client
import sys
import time
import urllib.parse

from watchdog.observers import Observer
import requests

from EventHandler import EventHandler


if __name__ == '__main__':
    paths = [ x for x in sys.argv[1:] ] or '.'
    print("The paths to be monitored are: ", paths)

    host = '140.160.107.111'
    port = '8080'

    url = "http://"+host+":"+port

    session = requests.Session()

    user = 'test'
    pwd = 'test'
    session.post(url+"/login",
                 data=("username="+user+"&"+"password="+pwd)
                 )

    r = session.get(url+"/api/tree")
    print(r.text)
#    print(json.dumps(eval(r.text), sort_keys=True,
#          indent=4, separators=(',',':')))



    event_handler = EventHandler(session, url)
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

