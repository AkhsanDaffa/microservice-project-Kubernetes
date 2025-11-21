from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is the API Service. Go to /api/data"

@app.route('/api/data')
def get_data():
    pod_name = os.environ.get('HOSTNAME','unknown')
    return jsonify(
        message="[Pesan dari Backend]",
        data="Hello, ini adalah data rahasia dari API Service!",
        server_pod=pod_name
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)