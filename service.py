## This is our main file 
from sender import sender
from listener import listener
from processor import processor 
# from preferences_panel import preferences
from falcon.falcon import SecretKey, PublicKey

import socket
import subprocess 
import logging
import csv
import sys
import threading

# Setting up Logging 
logging.basicConfig(filename="runtime.log",
                    format='%(levelname)s:%(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

## Helper functions 
def get_pub_key(ip_address):
    s = socket.create_connection((ip_address,1337))
    return s.recvmsg()

def remote_host_refresh(partial_ip,highest_address):
    remote_hosts = []
    for ping in range(2,highest_address):
        address = partial_ip + str(ping)
        res = subprocess.call(['ping', '-c', '3', address])
        if res == 0:
            logger.info( "ping to", address, "OK")
            remote_hosts.append(address)
        elif res == 2:
            logger.info("no response from {}.".format(str(address)))
        else:
            logger.warning("ping to", address, "failed!") 



## Startup Options
if len(sys.argv) == 1:
    sys.exit("ERROR : Too Few Arguments")
elif len(sys.argv) == 2:
    ## Starting / Stopping the node 
    if sys.argv[1] == "Start":
        running = True    
    elif sys.argv[1] == "Clear":
        running = False
        # clear out all global values here
        del remote_hosts
        del logger
        sys.exit("Service stopped running")
    else:
        sys.exit("ERROR : Invalid command {}".format(str(sys.argv)))
else:
    sys.exit("ERROR : Too Many Arguments")

## THIS SETS THE KEY SIZE. VALID (SECURE) OPTIONS: 512, 1024
GLOBAL_N = 512

## Register our node with the rest of the nodes 
# remote_hosts = [('192.168.0.20',5500)], ('192.168.0.30',5500), ('192.168.0.40',5500), ('192.168.0.50',5500), ('192.168.0.60',5500), ('192.168.0.70',5500), ('192.168.0.80',5500), ('192.168.0.90',5500)]
# Find where nodes are:
remote_host_update = threading.Thread(target=remote_host_refresh,args=('192.168.0.',254))
remote_host_update.start()

# generate pub / private key pair
if _secret_key:
    if _pub_key:
        logger.info("Key pair already created")
    else:
        logger.info("Creating public key")
        _pub_key = PublicKey(_secret_key)
else:
    logger.info("Creating key pair")
    _secret_key = SecretKey(GLOBAL_N)
    _pub_key = PublicKey(_secret_key)
    logger.info("Key pair created")

# Generate sender 
logger.info("Creating sender obj")
s = sender(_pub_key, _secret_key)
logger.info("Sender obj created")

# Send local public key 
pubKey_sharing = threading.Thread(target=s._share_pub_key,args=[len(remote_hosts)])
pubKey_sharing.start()
logger.info("Started sharing public key")

# # open listener for each remote host, add their pubkey to list
listeners = []
for host in remote_hosts:
    tmp_pubKey = get_pub_key(host[0])
    tmp_data_l = listener(host,5500,tmp_pubKey)
    tmp_key_l = listener(host,1337,tmp_pubKey)
    tmp_return_l = listener(host,6500,tmp_pubKey)
    listeners.append([tmp_data_l,tmp_pubKey,tmp_key_l,tmp_return_l])



## Constantly loop 
while running : 
    hosts_that_need_response = []
    ## Listen for data (to process/receiving) 
    for l in listeners:
        # if one of the hosts we are listening to is serving data
        if l[0].is_up():
            # connect and write the data to data_pre.csv
            data = l[0].connect()
            if data:
                processed_data = processor._process_data(data)
                s._send(processed_data,1,6500)
            else:
                print("Signature was invalid.")
                continue
        # if one of the hosts we are listening to is serving a new public key
        if l[2].is_up():
            # connect and update public key
            l[1] = l[2].connect()
        if l[3].is_up():
            data = l[3].connect()
            if data:
                with open('data_post.csv', 'w') as csvfile: 
                    csvwriter = csv.writer(csvfile) 
                    csvwriter.writerow(data)
            else:
                print("Signature was invalid.")
                continue

pubKey_sharing.join()
remote_host_update.join()

