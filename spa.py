from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder='dist', static_url_path='/')

CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(port = '5002',  host= '0.0.0.0', debug=False, threaded=True)