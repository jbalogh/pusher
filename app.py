import requests

from flask import Flask, request, jsonify
app = Flask(__name__)

db = {}


@app.route('/', methods=['GET'])
def root():
    return open('index.html').read()


@app.route('/queue', methods=['POST'])
def add_queue():
    user = request.form['user']
    queue = request.form['queue']
    db[user] = queue
    print db
    notify(queue, 'Welcome to PUSH!', 'So glad to have you, %s.' % user)
    return ''


@app.route('/message', methods=['POST'])
def send_message():
    name = request.form['user']
    message = request.form['message']
    title = 'Message from %s' % name
    names = []
    for user, queue in db.items():
        if name != user:
            notify(queue, title, message)
            names.append(user)
    return jsonify(title=title, message=message, names=names)


def notify(queue, title, text):
    print requests.post(queue, {'title': title, 'body': text})


if __name__ == '__main__':
    app.run(port=5002, debug=True)
