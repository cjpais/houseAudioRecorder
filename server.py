from subprocess import Popen
from flask import Flask, render_template
import var

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html") 

@app.route('/status/', methods=["POST", "GET"])
def status():
    return "status"

@app.route('/file/<int:id>/', methods=["POST", "GET"])
def getFile(id):
    return "file"

@app.route('/tags/', methods=["POST"])
def getTags():
    return "tags"

@app.route('/start/', methods=["POST"])
def start():
    if not var.recording:
        var.recording = Popen(["/usr/bin/sox", "-b", "16", "-e", "unsigned-integer",
                           "-r", "48k", "-c", "2", "-d", "--clobber", 
                           "1.mp3"])
        return "recording"
    return "not recording"

@app.route('/stop/', methods=["POST"])
def stop():
    print "recording var {}".format(var.recording)
    if var.recording:
        var.recording.terminate()
        return "stopped recording"
    else:
        return "no recording"

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
