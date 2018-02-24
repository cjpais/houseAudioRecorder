from subprocess import Popen
from datetime import datetime

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

    def start(self, n):
        self.name = n
        self.running = True
        self.date_created = self.date_modified = datetime.utcnow
        self.process = Popen(["/usr/bin/sox", "-b", "16", "-e", "unsigned-integer",
                              "-r", "48k", "-c", "2", "-d", "--clobber", 
                              "{}.mp3".format(self.name)])
        self.toggle = "Stop"

    def stop():
        self.name = ""
        self.running = False
        self.process = None
        self.toggle = "Start"
        self.tags = []

    def setName(self, n):
        self.date_modified = datetime.now
        self.name = n

    def setTags(self, ts):
        self.date_modified = datetime.now
        self.tags.append(ts)

    def getTags(self):
        return self.tags
         

recording = Recording()
