from flask import Flask, render_template, jsonify, request, url_for
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

@app.route('/toggle/', methods=["POST"])
def toggle():
    action = request.form['action']
    if action == "Start" and not recording.running:
        recording.start()
    elif action == "Stop" and recording.running:
        recording.stop()

    return recording.get_json()

"""
DB Helper Methods
"""

def getFiles():
    pass

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
