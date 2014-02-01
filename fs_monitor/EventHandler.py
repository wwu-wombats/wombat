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
        print(event.event_type)
        self.sync(event)

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
        pass


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
        pass


    def eventify(self, event_type):
        if event_type == 'modified':
            return "modify"
        elif event_type == "deleted":
            return "delete"
        elif event_type == "moved":
            return "move"
        elif event_type == "created":
            return "create"


    def sync(self, event):

        headers = {"Content-type" : "application/json"}
        event_thing = self.eventify(event.event_type)
        data = None
        if event.event_type == "moved":
            data = json.dumps({"payload" : '',
                               "src" : event.src_path,
                               "dest" : event.dest_path
                               })

        elif event.event_type == "created":
            f_data = None
            f_type = None
            if not event.is_directory:
                f_data = self.encrypt(event.src_path)
                f_type = "file"
            else:
                f_type = "dir"

            data = json.dumps({"payload" : f_data,
                               "t" : f_type
                               })

        elif event.event_type == "deleted":
            f_data = None
            f_type = None
            if not event.is_directory:
                f_type = "file"
            else:
                f_type = "dir"

            data = json.dumps({"payload" : event.src_path,
                               "t" : f_type,
                               "event" : "delete"
                               })
            self.connection.post(self.url+"/api/"+event_thing,
                                 data=data,
                                 headers=headers)
            return


        elif event.event_type == "modified":
            f_data = None
            f_type = None
            if not event.is_directory:
                f_data = self.encrypt(event.src_path)
                f_type = "file"
            else:
                return

            data = json.dumps({"payload" : f_data,
                               "t" : f_type
                               })


        self.connection.post(self.url+"/api/"+event_thing+event.src_path,
                             data=data,
                             headers=headers)




    def encrypt(self, path):
        with open(path, 'r') as f:
            return f.read()

