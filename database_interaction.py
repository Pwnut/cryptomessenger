import pyodbc
# database_interaction.py
# This script establishes a connection to the SQL Server database within the Docker container,
# verifies the connection, and lists all tables in the CryptomessengerDB database.
# It serves as a basic test for database connectivity and schema verification.

# Connection settings
server = 'localhost,1434'  # Change to the port if modified in Docker setup
database = 'CryptomessengerDB'
username = 'SA'
password = 'WeHacking808'  # Use the same SA password from the Docker setup

# Establish connection
try:
    connection = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    )
    print("Connection successful!")
except pyodbc.Error as e:
    print("Error in connection:", e)
    exit()

# Example query
cursor = connection.cursor()
cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(table.TABLE_NAME)

# Close the connection
connection.close()
