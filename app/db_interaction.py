import pyodbc
# db_interaction.py
# This script connects to the SQL Server database within the Docker container,
# performs sample data operations (inserting a user and retrieving users),
# and lists tables in the CryptomessengerDB database. 
# It is used for testing both connectivity and basic CRUD operations.

# Connection settings
server = 'sqlserver,1433'  # Adjust port if different
database = 'CryptomessengerDB'
username = 'SA'
password = 'WeHacking808'

# Establish connection
try:
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=YES;"
    )
    print("Connection successful!")
except pyodbc.Error as e:
    print("Error in connection:", e)
    exit()

cursor = conn.cursor()

# Example query: List all tables
cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(table.TABLE_NAME)

# Example: Insert a user
cursor.execute("INSERT INTO Users (Username, PublicKey, IsOnline) VALUES (?, ?, ?)", ('Alice', 'PublicKeyAlice', 1))
conn.commit()

# Example: Fetch all users
cursor.execute("SELECT * FROM Users")
for row in cursor.fetchall():
    print(row)

conn.close()
