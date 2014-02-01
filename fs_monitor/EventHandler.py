import json

#import requests

from watchdog.events import FileSystemEventHandler


class EventHandler(FileSystemEventHandler):
    def __init__(self, http_connection, url):
        # Persistent http connection
        self.connection = http_connection
        self.url = url

    def on_any_event(self, event):
        """
        On any event we want to possibly do logging. Anything else?
        """
        print(event)


    def on_moved(self, event):
        """
        On a move event a signal needs to be sent to the server to change a
        file's name and path.
        """
        pass


    def on_created(self, event):
        """
        On a create event we should just have to sync file to the server.
        """
        if event.is_directory:
            headers = {"Content-type" : "application/json"}
            self.connection.post(self.url+"/api/create/"+event.src_path,
                                 data=json.dumps({"payload" : event.src_path,
                                                  "event" : "directory_created"}),
                                 headers=headers)
        else:
            self.sync(event)


    def on_deleted(self, event):
        """
        On a delete event we would want to send a signal to the server to
        indicate that something has been deleted and remove it from the server
        """
        pass


    def on_modified(self, event):
        """
        On a modified event we want to update the file on the server with
        changes. Since we are worrying about encryption I cannot think of an
        easy way to only send diffs or something like that to save bandwidth.
        """
        if not event.is_directory:
            self.sync(event)


    def sync(self, event):
        f = open(event.src_path, "r")
        data = f.read()
        print("file created: ", event.src_path)


        headers = {"Content-type" : "application/json"}
        self.connection.post(self.url+"/api/create/"+event.src_path,
                             data=json.dumps({"payload" : data,
                                              "event" : event.event_type}),
                             headers=headers)
        f.close()



    def encypt(self):
        pass
