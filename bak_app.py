import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

DB_HOST = "192.168.210.148"
DB_PORT = 5432
DB_NAME = "afat_database"
DB_USER = "postgres"
DB_PASS = "test"

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        print("✅ Connected to PostgreSQL!")
        return conn
    except Exception as e:
        print("❌ Database connection failed:", e)
        return None

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Flask API!", 200

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "❌ Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        data = [dict(zip(column_names, row)) for row in rows]
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        print("❌ Error executing query:", e)
        return jsonify({"error": "❌ Failed to fetch users"}), 500
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)

