from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from multiprocessing import Process
from os.path import isfile
import socket

PUB_PATH='pub.pem'
PRIV_PATH='priv.pem'

def serialize_pub_key(key: bytes) -> bytes:
    return key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def serialize_priv_key(key: bytes) -> bytes:
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

def gen_key_pair():
    # Generate RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    private_pem = serialize_priv_key(private_key)
    public_pem = serialize_pub_key(public_key)

    with open(PRIV_PATH,'wb') as f:
        f.write(private_pem)
    with open(PUB_PATH,'wb') as f:
        f.write(public_pem)

def encrypt_message(msg: bytes, public_key: bytes) -> bytes:
    ciphertext = public_key.encrypt(
        msg,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA512()),
            algorithm=hashes.SHA512(),
            label=None
        )
    )
    return ciphertext

def decrypt_message(c_msg: bytes, private_key: bytes) -> bytes:
    plaintext = private_key.decrypt(
        c_msg,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA512()),
            algorithm=hashes.SHA512(),
            label=None
        )
    )
    return plaintext

def test_encryption(priv_key: bytes, pub_key: bytes):
    ct = encrypt_message(b'a message!', pub_key)
    print(ct)
    pt = decrypt_message(ct, priv_key)
    print(pt)

###
# simple online example. will it support several connections
# at once?
# Also, we're going to need a lot more work in order to parse
# the various messages we'll be sending over. We must develop
# some protocol that tells us what sort of data is coming in
# over the wire. ie-is it a public key, is it a message, receipt
# confirmation, so on and so forth.
###
def start_server():
    host = '0.0.0.0'  # unclean, only list correct interface
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print('Server listening on {}:{}'.format(host, port))

    while True:
        client_socket, client_address = server_socket.accept()
        print('Connection from:', client_address)

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print('Received:', data.decode())

            response = 'Message received'
            client_socket.sendall(response.encode())

        client_socket.close()

def send_message(remote_ip: str, msg: bytes):
    host = remote_ip  # Replace with the remote host's IP address
    port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.sendall(msg)

    data = client_socket.recv(1024)
    print('Received:', data.decode())

    client_socket.close()

if not isfile(PRIV_PATH) or not isfile(PUB_PATH):
    gen_key_pair()

private_key = None
public_key = None
with open(PRIV_PATH,'rb') as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)
with open(PUB_PATH,'rb') as f:
    public_key = serialization.load_pem_public_key(f.read())

test_encryption(private_key, public_key)
hostname = socket.gethostname()
ipaddr = socket.gethostbyname(hostname)

server_proc = Process(target=start_server)
server_proc.start()

# BE AWARE THAT THIS IS HARD CODED AND ASSUMES DOCKER WILL
# ASSIGN THE LOWEST AVAILABLE IP ADDRESSES FOR THE SAME NETWORK
# MASK. THIS IS ONLY FOR TESTING PURPOSES
hosts = ['.'.join(ipaddr.split('.')[0:3])+'.2', '.'.join(ipaddr.split('.')[0:3])+'.3']

pub_key_bytes = serialize_pub_key(public_key)

for ip in hosts:
    if ip != ipaddr:
        send_message(ip, pub_key_bytes)

#server_proc.join() # is this necessary? server doesn't end prematurely without it
