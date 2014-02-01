import http.client
import urllib.parse

from watchdog.events import FileSystemEventHandler


class EventHandler(FileSystemEventHandler):
    def __init__(self, http_connection):
        # Persistent http connection
        self.connection = http_connection


    def on_any_event(self, event):
        """
        On any event we want to possibly do logging. Anything else?
        """
        print(event)
#        headers = {"Contet-type" : "text/plain"}
#        self.conn.request("POST", '/', "this is data", headers)
#        response = self.conn.getresponse()
#        print(response.status, response.reason)
#        print(response.read())
#        conn.close()


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
        print("File created: ",event.src_path)



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
