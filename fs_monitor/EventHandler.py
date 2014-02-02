import json

from watchdog.events import FileSystemEventHandler


class EventHandler(FileSystemEventHandler):
    def __init__(self, http_connection, url, local_index, remote_index, prefix, sync_dir, pwd):
        self.connection = http_connection
        self.url = url
        self.prefix = prefix
        self.password = pwd
        self.sync_dir = sync_dir
        self.l_index = local_index
        self.r_index = remote_index

        self.sync_all(self.l_index['items'])


    def sync_all(self, items):
        for i in items:
            if i['t'] == 'file':
                self.man_upload(self.prefix + '/' + i['name'])
            if not i['items'] == []:
                self.sync_all(i['items'])



    def man_upload(self, path):
        print("uploading: ",path)
        headers = {"Content-type" : "application/json"}
        data = json.dumps({"payload" : self.encrypt(path),
                           "t" : 'file'
                           })
        self.connection.post(self.url+"/api/create/"+path,
                             data=data,
                             headers=headers)


    def on_any_event(self, event):
        print(event.event_type)
        self.sync(event)


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
            self.connection.post(self.url+"/api/"+event_thing,
                                 data=data,
                                 headers=headers)
            return


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

