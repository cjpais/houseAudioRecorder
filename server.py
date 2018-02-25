from flask import Flask, render_template, jsonify, request, url_for, send_from_directory
from subprocess import Popen, PIPE
from datetime import datetime
from pytz import timezone
import time
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////media/audio/recordings.db'
db = SQLAlchemy(app)
db.create_all()

@app.route('/')
def index():
    return render_template("index.html", recording=recording) 

@app.route('/ls/')
def list():
    recList = db.session.query(Recording).order_by(Recording.id.desc()).limit(25).all()
    dates = []
    for r in recList:
        dates.append(get_dt_str(r.date_created))
    return render_template("list.html", list=recList, dates=dates, status=recording) 

@app.route('/name/', methods=['POST'])
def rename():
    new_name = request.form['name']
    rec_id   = int(request.form['id'])
    if recording.running and rec_id == recording.id:
        recording.name = new_name
        print recording.name
        return recording.get_json()
    else:
        rec = db.session.query(Recording).filter_by(id=rec_id)
        rec.name = new_name
        db.session.commit()
        return url_for('list')

@app.route('/delete/', methods=['POST'])
def delete():
    rec_id = request.form['id']
    rec = db.session.query(Recording).filter_by(id=rec_id).first()
    os.remove(rec.filepath)
    db.session.delete(rec)
    db.session.commit()
    return url_for('list')

@app.route('/status/', methods=['POST'])
def status():
    return recording.get_json()

@app.route('/media/audio/<string:name>/', methods=["GET"])
def getFile(name):
    return send_from_directory('/media/audio/', name)

@app.route('/tags/', methods=["GET", "POST"])
def tags():
    tagList = db.session.query(Tag).all()
    return jsonify([t.get_json() for t in tagList])

@app.route('/tag/', methods=['POST'])
def tag():
    # TODO fix excessive code 
    print request.form

    if 'tagId' in request.form and 'recId' in request.form:
        rid = int(request.form['recId'])
        tid = int(request.form['tagId'])
        tag = db.session.query(Tag).filter(Tag.id == tid).first()

        if recording.running and recording.id == rid: 
            # add existing tag to new recording
            recording.tags.append(tag)
            return jsonify([t.get_json() for t in recording.tags]) 
        else:
            # get the recording and add existing tag to it
            print tag.name
            rec = db.session.query(Recording).filter(Recording.id == rid).first()
            rec.tags.append(tag)
            db.session.commit()
            return jsonify([t.get_json() for t in rec.tags])
    elif 'tagName' in request.form and 'recId' in request.form:
        rid = int(request.form['recId'])
        tagName = request.form['tagName']
        new_tag = Tag(name=tagName)
        if recording.running and recording.id == int(request.form['recId']):
            #add new tag to running recording
            recording.tags.append(new_tag)
            return jsonify([t.get_json() for t in recording.tags]) 
        else:
            # add new tag to existing recording
            rec = db.session.query(Recording).filter(Recording.id == rid).first()
            rec.tags.append(new_tag)
            db.session.commit()
            return jsonify([t.get_json() for t in rec.tags])
    elif 'tagName' in request.form:
        # add new tag and dont attach to any recording
        new_tag = Tag()
        new_tag.name = request.form['tagName']
        db.session.add(new_tag)
        db.session.commit()
        tagList = db.session.query(Tag).all()
        return jsonify([t.get_json() for t in tagList])
    return "you fucked up bro (aka i fucked up bro)"

@app.route('/tags/search/', methods=['POST'])
def searchTags():
    query = request.form['query']
    tagList = db.session.query(Tag).filter(Tag.name.ilike('%{}%'.format(query))).all()
    return jsonify([t.get_json() for t in tagList])

@app.route('/toggle/', methods=["POST"])
def toggle():
    action = request.form['action']
    if action == "start" and not recording.running:
        recording.start()
    elif action == "stop" and recording.running:
        recording.stop()

    return recording.get_json()

"""
HELPERS
"""

def get_dt_str(dt):
    utc = dt.replace(tzinfo = timezone('UTC'))
    pst = utc.astimezone(timezone('America/Los_Angeles'))
    return pst.strftime("%I:%M%p %m/%d/%Y")

"""
DB
"""

mm_tags_recs = db.Table('mm_tags_recs',
               db.Column('recording_id', db.Integer, db.ForeignKey('recording.id')),
               db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
               )

class Recording(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    filepath = db.Column(db.String, nullable=False)
    length = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    tags = db.relationship('Tag', secondary=mm_tags_recs, backref=db.backref('recordings'))

class currRec:
    def __init__(self, n = "", r = False, p = None, t = "Start"):
        self.id = 0
        self.name = n
        self.running = r
        self.process = p
        self.toggle = t
        self.date_created = None
        self.date_modified = None
        self.tags = []
        self.time = None

    def start(self):
        self.id = db.session.query(Recording).order_by(Recording.id.desc()).first().id + 1
        self.name = str(self.id)
        self.running = True
        self.date_created = self.date_modified = datetime.utcnow()
        self.time = time.time()
        DEVNULL = open(os.devnull, 'wb')
        self.process = Popen(["/usr/bin/sox", "-b", "16", "-e", "unsigned-integer",
                              "-r", "48k", "-c", "2", "-d", "--clobber", 
                              "/media/audio/{}.mp3".format(self.name)], stdout=DEVNULL)
        self.toggle = "Stop"

    def stop(self):
        self.process.terminate()
        # commit to db
        print self.name
        newRec = Recording(name=self.name, filepath="/media/audio/{}.mp3".format(self.id), length="fuck you")
        db.session.add(newRec)
        db.session.commit()
        # todo deal with tags...

        self.name = ""
        self.running = False
        self.process = None
        self.toggle = "Start"
        self.tags = []

    def set_name(self, n):
        self.date_modified = datetime.utcnow()
        self.name = n

    def set_tags(self, ts):
        self.date_modified = datetime.utcnow()
        self.tags.append(ts)

    def get_tags(self):
        return self.tags

    def get_json(self):
        return jsonify(
            id=self.id, 
            name=self.name, 
            running=self.running,
            toggle=self.toggle,
            time=self.time,
            tags=[t.get_json() for t in self.tags])

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

recording = currRec()

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    # datetime conversion for list
    app.jinja_env.globals.update(get_dt_str=get_dt_str)

