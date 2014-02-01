import http.client
import urllib.parse

from watchdog.events import FileSystemEventHandler


class EventHandler(FileSystemEventHandler):
    def __init__(self):
        # Some possible args will be a connection the sqlite database,
        # opening http connection (sockets?) for syncing.
        # Check in with the server for and changes (deletes, sync files, etc.)
        self.host = 'localhost'
        self.port = 9999
        self.conn = http.client.HTTPConnection(self.host, self.port)


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
