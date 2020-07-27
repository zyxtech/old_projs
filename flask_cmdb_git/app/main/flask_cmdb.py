from flask import Flask , send_from_directory

#app = Flask(__name__)
app = Flask(__name__, static_folder='static', static_url_path='/static')

#@app.route('/<path:path>')
#def send_static(path):
#    return send_from_directory('static', path)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
