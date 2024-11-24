from flask import Flask, request, jsonify
import pyodbc

# Flask application instance
app = Flask(__name__)

# Database configuration dictionary
DB_CONFIG = {
    'driver': 'ODBC Driver 17 for SQL Server',
    'server': '172.18.0.2,1433',  # Replace with your container's IP and port
    'database': 'CryptomessengerDB',
    'username': 'SA',
    'password': 'WeHacking808'
}

# Function to establish a connection to the SQL Server database
def get_db_connection():
    conn_str = f"DRIVER={DB_CONFIG['driver']};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};UID={DB_CONFIG['username']};PWD={DB_CONFIG['password']}"
    return pyodbc.connect(conn_str)

# Root route for basic connectivity check
@app.route('/')
def home():
    return "Welcome to the Cryptomessenger API!"

# Endpoint to register a user
@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.get_json()

    username = data.get('username')
    public_key = data.get('public_key')
    is_online = data.get('is_online')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert user details into the Users table
        cursor.execute("""
            INSERT INTO Users (Username, PublicKey, IsOnline)
            VALUES (?, ?, ?)
        """, (username, public_key, is_online))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "User registered successfully"}), 201

    except pyodbc.IntegrityError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to get a user by username
@app.route('/get_user', methods=['GET'])
def get_user():
    username = request.args.get('username')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Retrieve user details based on the provided username
        cursor.execute("""
            SELECT Username, PublicKey, IsOnline
            FROM Users
            WHERE Username = ?
        """, (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify({
                "username": user[0],
                "public_key": user[1],
                "is_online": bool(user[2])
            }), 200
        else:
            return jsonify({"message": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0')
