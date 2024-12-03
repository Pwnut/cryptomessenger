from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from os.path import isfile
from db_api import delete_user, register_user

PUB_PATH='pub.pem'
PRIV_PATH='priv.pem'

private_key = None
public_key = None

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

def unserialize_pub_key(serialized_key: bytes) -> bytes:
    return serialization.load_pem_public_key(serialized_key)

def unserialize_priv_key(serialized_key: bytes) -> bytes:
    return serialization.load_pem_private_key(serialized_key, password=None)

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

if not isfile(PRIV_PATH) or not isfile(PUB_PATH):
    gen_key_pair()

with open(PRIV_PATH,'rb') as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

with open(PUB_PATH,'rb') as f:
    public_key = serialization.load_pem_public_key(f.read())
# repopulate this every time we boot
delete_user('127.0.0.1')
register_user('127.0.0.1', serialize_pub_key(public_key))
