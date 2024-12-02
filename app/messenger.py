from multiprocessing import Process, Queue
import server
import client
import db_api
import db_api

queue = Queue()
Process(target=server.start_messenger_server,args=(queue,),kwargs={"port":5001}).start()
