# Navigate to the project directory
cd /path/to/your/project

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python3 app.py
### `register_user(ip, public_key, username)`
Register a new user with the given IP address, public key, and username.

### `get_user(username=None)`
Retrieve all users if no `username` is provided. If a `username` is specified, retrieve details for that user.

### `get_pub_key(ip)`
Fetch the public key for a given IP address.

### `get_priv_key()`
Fetch the private key for the current node.

### `save_message(ip, timestamp, message_id, message)`
Save a message to the database.

### `delete_user(username)`
Delete a user and all related messages.

---

## Example Usage

### Register a User
```python
from API import register_user
print(register_user('192.168.1.2', 'PublicKey', username='TestUser')
