## This tests the connect and receive data functions
from listener import listener
import time 
from falcon.falcon import PublicKey, SecretKey 


prv_key = SecretKey(512)
pubKey = PublicKey(prv_key)

#valid data and sender 
l = listener(('192.168.0.4',5500),pubKey)
print("Setup done\n")

if l.is_up():
	print("Host is up!\n")
	b = time.time()
	data = l.connect()
	e = time.time()
	print("It took {} seconds to connect and receive data.\n".format(e - b))
	print(data)
	

