from falcon.falcon import PublicKey, SecretKey
import socket
import random
import logging
import os 

# Setting up Logging 
logging.basicConfig(filename="listener_runtime.log",
                            format='%(levelname)s:%(message)s',
                            filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class listener():
    ip_address = '127.0.0.1'
    port = 5500
    sk = SecretKey(512)
    pubKey = PublicKey(sk)

    def __init__(self,ip,port,key):
        self.ip_address = ip
        self.port = port
        self.pubKey = key

    def is_up(self):
        # Check to see if a remote host is trying to share data 
        resp = os.system("telnet " + self.ip_address + " " + str(self.port))
        if resp == 0:
            logger.info("{} is up and listening on port {}.".format(self.ip_address,self.port))
            return True
        else:
            logger.info("Port {} is not open on {}".format(self.port,self.ip_address))
            return False

    def connect(self):
        # Connect and receive data from remote host
        s = socket.create_connection((self.ip_address,self.port))
        data = s.recvmsg()
        signature = s.recvmsg()
        if self.pubKey.verify(data,signature):
            return data
        else:
            logger.error("The signature is INVALID")
            return None