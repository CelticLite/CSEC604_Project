## This tests the share function
from falcon.falcon import PublicKey, SecretKey 
from sender import sender
import time 

#valid data and sender 
data = b"hello"
prv_key = SecretKey(512)
pubKey = PublicKey(prv_key)
s = sender(pubKey,prv_key)
print("Setup done\n")

s._send([data,0],1)
print("sent successfully")