from flask import Flask
import flask


app = Flask(__name__)

global record

def sendEvents():
    record=0
    while(1):
        yield 'data: \t recordNum'+ str(record) +' hello from api!'

@app.route('/messages', methods=['GET'])
def stream():
    return flask.Response(sendEvents(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)