from proto import messaging_pb2
from time import time
from uuid import uuid4
import socket
import multiprocessing
from queue import Queue
from encryption import encrypt_message, decrypt_message

# Store recipient status and offline messages
recipient_servers = {}  # {username: (host, port)}
offline_messages = {}  # {username: [messages]}

def create_header():
    return messaging_pb2.Header(timestamp=int(time()), message_id=str(uuid4()))

def handle_client(conn, addr, queue):
    # Register recipient server
    size_bytes = conn.recv(4)
    message_size = int.from_bytes(size_bytes, 'big')
    print(f'MESSAGE SIZE: {message_size}')
    message_data = conn.recv(message_size)
    received_message = messaging_pb2.MessageWrapper()
    received_message.ParseFromString(message_data)
    if received_message.HasField('reg'):
        print(f"Registration Info for {received_message.reg.name}")
        print(f"{received_message.reg.pub_key}")
        print('')
        queue.put((dummy_func, ['reg received']))
        # TODO
        #our_name, our_pub_key = getRegInfo()
        our_name, our_pub_key = ('TEST','TEST')
        reg_resp = messaging_pb2.MessageWrapper(reg=messaging_pb2.RegInfo(
                                                    header=create_header(),
                                                    name=our_name,
                                                    pub_key=our_pub_key
                                                )
                                            )
        serialized_resp = reg_resp.SerializeToString()
        conn.sendall(len(serialized_resp).to_bytes(4, 'big') + serialized_resp)
    elif received_message.HasField('enc_msg'):
        print(f"Encrypted Message: {received_message.enc_msg.ciphertext}")
        print('')
        queue.put((dummy_func, ['enc_msg received']))
        dec_msg = decrypt_message(received_message.enc_msg.ciphertext)
        msg = messaging_pb2.Message()
        msg.ParseFromString(dec_msg)
        print(msg.plaintext)
        acked_mid = msg.header.message_id
        msg_ack = messaging_pb2.MessageAck(header=create_header(), acked_mid=acked_mid)
        ciphertext = encrypt_message(addr[0], msg_ack.SerializeToString())
        enc_msg = messaging_pb2.EncryptedMessage(ciphertext=ciphertext)
        response = messaging_pb2.MessageWrapper(enc_msg=enc_msg)
        serialized_resp = response.SerializeToString()
        conn.sendall(len(serialized_resp).to_bytes(4, 'big') + serialized_resp)
    elif received_message.HasField('ping'):
        queue.put((dummy_func, ['ping received']))
        response = messaging_pb2.MessageWrapper(pong=True)
        serialized_resp = response.SerializeToString()
        conn.sendall(len(serialized_resp).to_bytes(4, 'big') + serialized_resp)
    conn.close()

def forward_message(sender, recipient, message_body):
    if recipient in recipient_servers:
        recipient_host, recipient_port = recipient_servers[recipient]
        try:
            # Forward message to recipient server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((recipient_host, recipient_port))
                s.send(f"{sender}:{message_body}".encode('utf-8'))
                print(f"Message sent to {recipient}")
        except ConnectionRefusedError:
            print(f"{recipient} server is offline. Storing message.")
            store_offline_message(recipient, f"{sender}:{message_body}")
    else:
        print(f"{recipient} is not registered. Storing message.")
        store_offline_message(recipient, f"{sender}:{message_body}")


def store_offline_message(username, message):
    if username not in offline_messages:
        offline_messages[username] = []
    offline_messages[username].append(message)

def dummy_func(arg):
    print(f'In dummy func: {arg}')

def dispatcher(queue):
    while True:
        func, params = queue.get()
        func(*params)

def start_messenger_server(host='127.0.0.1', port=5000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"Central server started on {host}:{port}")

    queue = multiprocessing.Queue()
    multiprocessing.Process(target=dispatcher, args=(queue,))
    while True:
        conn, addr = server.accept()
        multiprocessing.Process(target=handle_client, args=(conn, addr, queue)).start()
