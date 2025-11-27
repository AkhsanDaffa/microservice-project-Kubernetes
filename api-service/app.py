# from flask import Flask, jsonify
# import os

# app = Flask(__name__)

# is_healthy = True

# @app.route('/')
# def home():
#     return "Hello, this is the API Service. Go to /api/data"

# @app.route('/api/data')
# def get_data():
#     pod_name = os.environ.get('HOSTNAME','unknown')
#     return jsonify(
#         message="[Pesan dari Backend]",
#         data="Hello, ini adalah data rahasia dari API Service!",
#         server_pod=pod_name
#     )

# @app.route('/health')
# def health_check():
#     if is_healthy:
#         return "I am healthy", 200
#     else:
#         return "I am broken", 500

# @app.route('/sabotage')
# def sabotage():
#     global is_healthy
#     is_healthy = False
#     return "Service sabotaged! Health check will now fail.", 200

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

############## Step 2 : Implementasi Database #################
from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'flask_db')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASS', 'passwordrahasia')

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('CREATE TABLE IF NOT EXISTS visitors (id SERIAL PRIMARY KEY, count INTEGER);')
        cur.execute('SELECT count FROM visitors WHERE id=1;')

        if cur.fetchone() is None:
            cur.execute('INSERT INTO visitors (id, count) VALUES (1, 0);')
        
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully.")

    except Exception as e:
        print(f"Error initializing database: {e}")

init_db()

@app.route('/')
def home():
    return "Hello, Go to /api/visit to count me."

@app.route('/health')
def health_check():
    return "I am healthy", 200

@app.route('/api/visit')
def visit():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute('UPDATE visitors SET count = count + 1 WHERE id=1;')

        cur.execute('SELECT count FROM visitors WHERE id=1;')
        visit_count = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        pod_name = os.environ.get('HOSTNAME','unknown')
        return jsonify(
            message="Kunjungan tercatat!",
            visit_count=visit_count,
            server_pod=pod_name
        )

    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)