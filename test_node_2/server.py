from proto import messaging_pb2
from time import time
from uuid import uuid4
import socket
import multiprocessing
from queue import Queue
from db_api import *
from encryption import *

# Store recipient status and offline messages
recipient_servers = {}  # {username: (host, port)}
offline_messages = {}  # {username: [messages]}

def create_header():
    return messaging_pb2.Header(timestamp=int(time()), message_id=str(uuid4()))

def handle_client(conn, addr, queue):
    # Register recipient server
    size_bytes = conn.recv(4)
    message_size = int.from_bytes(size_bytes, 'big')
    message_data = conn.recv(message_size)
    received_message = messaging_pb2.MessageWrapper()
    received_message.ParseFromString(message_data)
    if received_message.HasField('reg'):
        register_user(addr[0], received_message.reg.pub_key.decode(), username=addr[0])
        queue.put({'type':'new_user', 'sender_ip':addr[0]})
        ser_pub_key = serialize_pub_key(public_key)
        reg_resp = messaging_pb2.MessageWrapper(reg=messaging_pb2.RegInfo(
                                                    header=create_header(),
                                                    pub_key=ser_pub_key
                                                    )
                                                )
        serialized_resp = reg_resp.SerializeToString()
        conn.sendall(len(serialized_resp).to_bytes(4, 'big') + serialized_resp)
    elif received_message.HasField('enc_msg'):
        print(f"Encrypted Message: {received_message.enc_msg.ciphertext}")
        print('')
        pub_key = get_pub_key(addr[0])
        if "error" in pub_key:
            print("No public key registered")
        else:
            dec_msg = decrypt_message(received_message.enc_msg.ciphertext, private_key)
            msg = messaging_pb2.Message()
            msg.ParseFromString(dec_msg)
            mid = msg.header.message_id
            new_msg = msg.plaintext
            queue.put({'type':'new_msg', 'sender_ip':addr[0], 'message_id':mid, 'new_msg':new_msg})
            msg_ack = messaging_pb2.MessageAck(header=create_header(), acked_mid=mid)
            unser_pub_key = unserialize_pub_key(get_pub_key(addr[0]).encode())
            ciphertext = encrypt_message(msg_ack.SerializeToString(), unser_pub_key)
            enc_msg = messaging_pb2.EncryptedMessage(ciphertext=ciphertext)
            response = messaging_pb2.MessageWrapper(enc_msg=enc_msg)
            serialized_resp = response.SerializeToString()
            conn.sendall(len(serialized_resp).to_bytes(4, 'big') + serialized_resp)
    elif received_message.HasField('ping'):
        queue.put({'type':'user_online', 'sender_ip':addr[0]})
        response = messaging_pb2.MessageWrapper(pong=True)
        serialized_resp = response.SerializeToString()
        conn.sendall(len(serialized_resp).to_bytes(4, 'big') + serialized_resp)
    conn.close()

def start_messenger_server(queue, host='0.0.0.0', port=5000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"Central server started on {host}:{port}")

    while True:
        conn, addr = server.accept()
        multiprocessing.Process(target=handle_client, args=(conn, addr, queue,)).start()
