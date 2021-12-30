from flask import Flask
import flask
import time

app = Flask(__name__)

global record

def sendEvents():
    record=0
    while(1):
        record+=1
        time.sleep(3)
        yield 'data: \t recordNum'+ str(record) +' hello from api!'

@app.route('/messages', methods=['GET'])
def stream():
    return flask.Response(sendEvents(), mimetype='text/event-stream')

@app.route('/', methods=['GET'])
def index():
    return '<H3>Please hit /messages path to get message streams.</H3>'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)