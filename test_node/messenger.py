from multiprocessing import Process, Queue
import server
import client
from time import sleep

queue = Queue()
Process(target=server.start_messenger_server,args=(queue,),kwargs={"port":5000}).start()

while True:
    event_dict = queue.get()
    if event_dict['type'] == 'new_msg':
        sleep(2)
        client.send_message('well hi there!', host=event_dict['sender_ip'])
