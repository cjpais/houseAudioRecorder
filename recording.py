from subprocess import Popen
from datetime import datetime
from flask import jsonify

class Recording:
    # really this is going to be database class that we use everywhere
    # on stop we will commit to the db the new tags and recording name
    # this is just setting up the class

    def __init__(self, n = "", r = False, p = None, t = "Start"):
        self.id = 0
        self.name = n
        self.running = r
        self.process = p
        self.toggle = t
        self.date_created = None
        self.date_modified = None
        self.tags = []

    def start(self):
        self.name = 1
        self.running = True
        self.date_created = self.date_modified = datetime.utcnow
        self.process = Popen(["/usr/bin/sox", "-b", "16", "-e", "unsigned-integer",
                              "-r", "48k", "-c", "2", "-d", "--clobber", 
                              "/media/audio/{}.mp3".format(self.name)])
        self.toggle = "Stop"

    def stop(self):
        self.name = ""
        self.running = False
        self.process.terminate()
        self.process = None
        self.toggle = "Start"
        self.tags = []

    def set_name(self, n):
        self.date_modified = datetime.now
        self.name = n

    def set_tags(self, ts):
        self.date_modified = datetime.now
        self.tags.append(ts)

    def get_tags(self):
        return self.tags

    def get_json(self):
        return jsonify(
            id=self.id, 
            name=self.name, 
            running=self.running,
            toggle=self.toggle,
            tags=self.tags)
         

recording = Recording()
