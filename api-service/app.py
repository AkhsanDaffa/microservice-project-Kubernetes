from flask import Flask, jsonify
import os

app = Flask(__name__)

is_healthy = True

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

@app.route('/health')
def health_check():
    if is_healthy:
        return "I am healthy", 200
    else:
        return "I am broken", 500

@app.route('/sabotage')
def sabotage():
    global is_healthy
    is_healthy = False
    return "Service sabotaged! Health check will now fail.", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)