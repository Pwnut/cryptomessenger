import pyodbc
from datetime import datetime

# Database configuration dictionary
DB_CONFIG = {
    'driver': 'ODBC Driver 18 for SQL Server',
    'server': 'sqlserver,1433',  # Use the container's IP
    'database': 'CryptomessengerDB',
    'username': 'SA',
    'password': 'WeHacking808',
    'TrustServerCertificate': 'YES',
    'Encrypt': 'NO',  # Disable encryption to avoid certificate validation issues
}

# Function to establish a connection to the SQL Server database
def get_db_connection():
    conn_str = (
        f"DRIVER={{{DB_CONFIG['driver']}}};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']};"
        f"TrustServerCertificate={DB_CONFIG['TrustServerCertificate']};"
        f"Encrypt={DB_CONFIG['Encrypt']};"
    )
    print(f"Using connection string: {conn_str}")  # Log the connection string for debugging
    return pyodbc.connect(conn_str, timeout=10)

# Function to register a new user with their IP, public key, and username
def register_user(ip, public_key, is_online=1, username=None):
    try:
        if not username:
            username = ip  # Use IP as the default username if none is provided
        
        print("Establishing database connection...")
        conn = get_db_connection()
        print("Database connection established.")
        
        cursor = conn.cursor()
        print("Executing SQL query to register user...")
        print(f'{ip}:{public_key}:{username}')
        cursor.execute("""
            INSERT INTO Users (Username, IP, PublicKey, IsOnline)
            VALUES (?, ?, ?, ?)
        """, (username, ip, public_key, is_online))
        conn.commit()
        print("Query executed successfully. User registered.")
        
        cursor.close()
        conn.close()
        return {"message": f"User '{username}' with IP '{ip}' registered successfully."}

    except pyodbc.IntegrityError as e:
        print(f"IntegrityError occurred: {e}")
        return {"error": f"IntegrityError: {str(e)}"}
    except Exception as e:
        print(f"Error occurred: {e}")
        return {"error": str(e)}

# Function to retrieve a user's details by username
def get_user(username=None):  # Add default value of None for username
    try:
        print("Establishing database connection...")
        conn = get_db_connection()
        print("Database connection established.")
        
        cursor = conn.cursor()
        
        if username:
            print(f"Executing SQL query to retrieve user '{username}'...")
            cursor.execute("""
                SELECT Username, PublicKey, IsOnline
                FROM Users
                WHERE Username = ?;
            """, (username,))
        else:
            print("Executing SQL query to retrieve all users...")
            cursor.execute("""
                SELECT Username, PublicKey, IsOnline
                FROM Users;
            """)
        
        users = cursor.fetchall()
        cursor.close()
        conn.close()

        if not users:
            print("No users found.")
            return []

        print("Users retrieved successfully.")
        return [
            {
                "username": user[0],
                "public_key": user[1],
                "is_online": bool(user[2])
            }
            for user in users
        ]

    except Exception as e:
        print(f"Error occurred: {e}")
        return {"error": str(e)}


def delete_user(username):
    try:
        print("Establishing database connection...")
        conn = get_db_connection()
        print("Database connection established.")
        
        cursor = conn.cursor()
        print(f"Executing SQL queries to delete user '{username}' and related messages...")
        
        # Get UserID of the user
        cursor.execute("""
            SELECT UserID FROM Users WHERE Username = ?;
        """, (username,))
        user = cursor.fetchone()
        if not user:
            return {"error": f"User '{username}' does not exist."}
        user_id = user[0]
        
        # Delete related messages
        cursor.execute("""
            DELETE FROM Messages WHERE SenderID = ? OR RecipientID = ?;
        """, (user_id, user_id))
        
        # Delete the user
        cursor.execute("""
            DELETE FROM Users WHERE Username = ?;
        """, (username,))
        conn.commit()
        
        print(f"User '{username}' and related records deleted successfully.")
        cursor.close()
        conn.close()
        return {"message": f"User '{username}' and related records deleted successfully."}

    except Exception as e:
        print(f"Error occurred: {e}")
        return {"error": str(e)}
# Function to fetch the public key for a given IP address
def get_pub_key(ip):
    try:
        print("Establishing database connection...")
        conn = get_db_connection()
        print("Database connection established.")

        cursor = conn.cursor()
        print(f"Executing SQL query to retrieve public key for IP '{ip}'...")
        cursor.execute("""
            SELECT PublicKey
            FROM Users
            WHERE IP = ?
        """, (ip,))
        public_key = cursor.fetchone()
        cursor.close()
        conn.close()

        if public_key:
            print(f"Public key for IP '{ip}' found.")
            return public_key[0]  # Return the public key as a string
        else:
            print(f"No public key found for IP '{ip}'.")
            return {"error": f"No public key found for IP '{ip}'."}
    except Exception as e:
        print(f"Error occurred: {e}")
        return {"error": str(e)}

def get_priv_key():
    # Placeholder implementation for private key retrieval
    try:
        # Normally, you would retrieve the private key securely from a file or secure storage
        return {"error": "Private key retrieval is not implemented in this API."}
    except Exception as e:
        return {"error": str(e)}

# Function to save a message to the database
def save_message(sender_ip, recipient_ip, timestamp, message_id, message):
    try:
        print("Establishing database connection...")
        conn = get_db_connection()
        print("Database connection established.")
        
        cursor = conn.cursor()
        print("Executing SQL query to save message...")
        cursor.execute("""
            INSERT INTO Messages (SenderID, RecipientID, Timestamp, MessageID, MessageContent)
            VALUES (
                (SELECT UserID FROM Users WHERE IP = ?), (SELECT UserID FROM Users WHERE IP = ?), ?, ?, ?
            )
        """, (sender_ip, recipient_ip, timestamp, message_id, message))
        conn.commit()
        print("Query executed successfully. Message saved.")
        
        cursor.close()
        conn.close()
        return {"message": "Message saved successfully."}

    except Exception as e:
        print(f"Error occurred: {e}")
        return {"error": str(e)}

# Optional debugging entry point for manual testing
if __name__ == "__main__":
    # General user registration and retrieval test
    print(register_user("DebugUser", "DebugPublicKey", 1))
    print(get_user("DebugUser"))
    
    # Fetch public key by IP test
    print(get_pub_key("192.168.1.1"))
    
    # Save a message test
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(save_message("192.168.1.1", timestamp, "msg001", "This is a test message."))
    
    # Fetch private key (not implemented)
    print(get_priv_key())
