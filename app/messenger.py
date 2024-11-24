from multiprocessing import Process
import server
import client

Process(target=server.start_messenger_server,args=()).start()
