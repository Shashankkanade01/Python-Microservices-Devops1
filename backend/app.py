import time
import psycopg2
from flask import Flask, jsonify, request   # <-- added request here
import os
import logging

app = Flask(__name__)

# PostgreSQL config
DB_HOST = os.environ.get("DB_HOST", "postgres")
DB_NAME = os.environ.get("DB_NAME", "mydb")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_PORT = os.environ.get("DB_PORT", 5432)

# Logging setup
LOG_FILE = "/logs/app.log"
os.makedirs("/logs", exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# --- DB connection with retry ---
def get_db_connection():
    retries = 10
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                port=DB_PORT
            )
            return conn
        except psycopg2.OperationalError as e:
            logging.warning(f"Postgres not ready, retrying in 3s... ({retries} left)")
            retries -= 1
            time.sleep(3)
    raise Exception("Cannot connect to Postgres after multiple retries.")

# Initialize table
conn = get_db_connection()
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        email VARCHAR(50)
    );
""")
conn.commit()
cur.close()
conn.close()
logging.info("Database initialized.")

# --- API endpoints ---

# Fetch all users
@app.route("/api/data")
def get_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    logging.info("/api/data called")
    return jsonify(rows)

# Add a new user
@app.route("/api/add_user", methods=["POST"])
def add_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cur.close()
    conn.close()

    logging.info(f"New user added: {name}, {email}")
    return jsonify({"message": "User added successfully!"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
