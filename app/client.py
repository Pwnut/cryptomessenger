import socket
from time import time
from uuid import uuid4
from multiprocessing import Manager
from proto import messaging_pb2
from time import sleep
from db_api import *
from encryption import *

manager = Manager()
# dict of host ips that have unsent messages. Each ip is a key
# to a Manager.list() of messages queued up to be sent
unsent_lists = {}

def create_header():
    return messaging_pb2.Header(timestamp=int(time()), message_id=str(uuid4()))

def send_packet(packet_data, host='127.0.0.1', port=5000):
    serialized_packet = packet_data.SerializeToString()
    packet = len(serialized_packet).to_bytes(4, 'big') + serialized_packet
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(5)
            s.bind(('0.0.0.0',5002))
            s.connect((host, port))

            s.send(packet)

            size_bytes = s.recv(4)
            resp_size = int.from_bytes(size_bytes, 'big')
            resp_data = s.recv(resp_size)
            received_message = messaging_pb2.MessageWrapper()
            received_message.ParseFromString(resp_data)
            return received_message
    except ConnectionRefusedError:
        return "ConnectionRefusedError"
    except:
        return None

def send_message(pm, host='127.0.0.1', port=5000, preview=False):
    msg = messaging_pb2.Message(header=create_header(),
                                        plaintext=pm
                                    )
    serialized_msg = msg.SerializeToString()
    pub_key = get_pub_key(host)
    if "error" in pub_key:
        return False
    unser_pub_key = unserialize_pub_key(pub_key.encode())
    ciphertext = encrypt_message(serialized_msg, unser_pub_key)
    if preview:
        return ciphertext
    enc_msg = messaging_pb2.EncryptedMessage(ciphertext=ciphertext)
    wrapped_msg = messaging_pb2.MessageWrapper(enc_msg=enc_msg)
    response = send_packet(wrapped_msg, host=host, port=port)
    if response is None:
        return False
    else:
        ciphertext = response.enc_msg.ciphertext
        serialized_ack = decrypt_message(ciphertext, private_key)
        ack = messaging_pb2.MessageAck()
        ack.ParseFromString(serialized_ack)
        timestamp = ack.header.timestamp
        mid = ack.header.message_id
        # not using this atm
        acked_mid = ack.acked_mid 
        return acked_mid

def send_ping(host='127.0.0.1', port=5000):
    ping = messaging_pb2.MessageWrapper(ping=True)
    response = send_packet(ping, host=host, port=port)
    if response is None:
        return False
    else:
        if response.HasField('pong'):
            return True
        else: # didnt get reg (or complete reg) message back
            return False

def send_reg_request(host='127.0.0.1', port=5000):
    # TODO
    ser_pub_key = serialize_pub_key(public_key)
    req = messaging_pb2.MessageWrapper(reg=messaging_pb2.RegInfo(
                                                header=create_header(),
                                                pub_key=ser_pub_key
                                            )
                                       )
    response = send_packet(req, host=host, port=port)
    if response is None:
        return False
    else:
        if response.HasField('reg'):
            print(f'pub key on client side: {response.reg.pub_key}')
            # TODO
            return register_user(host, response.reg.pub_key.decode())
        else: # didnt get reg (or complete reg) message back
            return False

