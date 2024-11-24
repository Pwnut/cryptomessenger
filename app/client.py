import socket
from time import time
from uuid import uuid4
from multiprocessing import Manager
from proto import messaging_pb2
from time import sleep
from encryption import encrypt_message, decrypt_message

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
            s.connect((host, port))

            s.send(packet)

            size_bytes = s.recv(4)
            resp_size = int.from_bytes(size_bytes, 'big')
            resp_data = s.recv(resp_size)
            received_message = messaging_pb2.MessageWrapper()
            received_message.ParseFromString(resp_data)
            return received_message
    except ConnectionRefusedError:
        print(f'{host} not available')
        return None

def send_message(pm, host='127.0.0.1', port=5000):
    msg = messaging_pb2.Message(header=create_header(),
                                        plaintext=pm
                                    )
    serialized_msg = msg.SerializeToString()
    ciphertext = encrypt_message(host, serialized_msg)
    enc_msg = messaging_pb2.EncryptedMessage(ciphertext=ciphertext)
    wrapped_msg = messaging_pb2.MessageWrapper(enc_msg=enc_msg)
    response = send_packet(wrapped_msg)
    if response is None:
        return False
    else:
        ciphertext = response.enc_msg.ciphertext
        serialized_ack = decrypt_message(ciphertext)
        ack = messaging_pb2.MessageAck()
        ack.ParseFromString(serialized_ack)
        timestamp = ack.header.timestamp
        mid = ack.header.message_id
        acked_mid = ack.acked_mid 
        print(acked_mid)

def ping(host='127.0.0.1', port=5000):
    ping = messaging_pb2.MessageWrapper(ping=True)
    response = send_packet(ping)
    if response is None:
        return False
    else:
        if response.HasField('pong'):
            return True
        else: # didnt get reg (or complete reg) message back
            return False

#def retry_send(host, port, unsent_packets):
#    for p in unsent_packets:
#        try:
#            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#                s.connect((central_host, central_port))
#
#                s.send(packet)
#
#                size_bytes = s.recv(4)
#                resp_size = int.from_bytes(size_bytes, 'big')
#                resp_data = client_socket.recv(resp_size)
#                received_message = messaging_pb2.MessageWrapper()
#                received_message.ParseFromString(message_data)
#                return received_message
#        except ConnectionRefusedError:
#            sleep(2)

#def send_when_up(message, host='127.0.0.1', port=5000):
#    if host in unsent_lists:
#        unsent_lists[host].append(message)
#    else:
#        new_unsent_list = manager.list()
#        new_unsent_list.append(message)
#        unsent_lists[host] = new_unsent_list
#        multiprocessing.Process(target=retry_send, args=(host, port, new_unsent_list))

def send_reg_request(host='127.0.0.1', port=5000):
    # TODO
    #our_name, our_pub_key = getRegInfo()
    our_name, our_pub_key = ('TEST','TEST')
    req = messaging_pb2.MessageWrapper(reg=messaging_pb2.RegInfo(
                                                header=create_header(),
                                                name=our_name,
                                                pub_key=our_pub_key
                                            )
                                       )
    response = send_packet(req)
    if response is None:
        return False
    else:
        if response.HasField('reg'):
            new_user = response.reg.name
            new_pub_key = response.reg.pub_key
            # TODO
            #register_user(host, new_user, new_pub_key)
            return True
        else: # didnt get reg (or complete reg) message back
            return False

