from subprocess import Popen, PIPE
from datetime import datetime
from time import mktime
from flask import jsonify
from server import db 
from flask_sqlalchemy import SQLAlchemy

tags = db.Table('tags',
        db.Column('recording_id', db.Integer, db.ForeignKey('recordings.id')),
        db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
        )

class Recording(db.Model):
    __tablename__ = "recordings"

    id = db.column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    filepath = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    date_modified = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    tags = db.relationship('tags', secondary=tags, backref=db.backref('recordings'))

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
                              "/media/audio/{}.mp3".format(self.name)], stdout=PIPE)
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
            date_created=mktime(self.date_created.timetuple()),
            tags=self.tags)

class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

         
recording = Recording()
