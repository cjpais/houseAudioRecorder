from flask import Flask, render_template, jsonify
from recording import recording 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", recording=recording) 

@app.route('/ls/')
def list():
    return render_template("list.html") 

@app.route('/file/<int:id>/', methods=["POST", "GET"])
def getFile(id):
    pass

@app.route('/tags/<string:s>/', methods=["POST"])
def tags(s):
    pass

@app.route('/start/', methods=["POST"])
def start():
    if not recording.running:
        recording.start()
    return jsonify(recording)

@app.route('/stop/', methods=["POST"])
def stop():
    print "recording var {}".format(var.recording)
    if recording.running:
        recording.stop()
    return jsonify(recording)

"""
DB Helper Methods
"""

def getFiles():
    pass


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
