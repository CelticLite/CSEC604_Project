# Test script for Signing data 
from falcon.falcon import PublicKey, SecretKey 
from sender import sender
import time 

data = bytearray([3,4,5,6,7,8])
avg_prv_key_time = 0 
avg_pub_key_time = 0 
avg_sender_time = 0 
avg_sign_time = 0 



for i in range(0,99):
	secret_begin = time.time()
	prv_key = SecretKey(512)
	secret_end = time.time()
	print("Creating private key took {} seconds".format(secret_end - secret_begin))
	avg_prv_key_time += secret_end - secret_begin

	public_begin = time.time()
	pubKey = PublicKey(prv_key)
	public_end = time.time()
	print("Creating public key took {} seconds".format(public_end - public_begin))
	avg_pub_key_time += public_end - public_begin

	sender_begin = time.time()
	s = sender(pubKey,prv_key)
	sender_end = time.time()
	print("Creating sender object for data share took {} seconds".format(sender_end - sender_begin))
	avg_sender_time += sender_end - sender_begin

	sign_begin = time.time()
	sig = s._sign(data)
	sign_end = time.time()
	print("Signing your data took {} seconds.".format(sign_end - sign_begin))
	avg_sign_time += sign_end - sign_begin

avg_prv_key_time = avg_prv_key_time / 100.0 
avg_pub_key_time = avg_pub_key_time / 100.0 
avg_sender_time = avg_sender_time / 100.0
avg_sign_time = avg_sign_time / 100.0

print("AVERAGE TIME TO CREATE PRIVATE KEY : {}".format(avg_prv_key_time)) 
print("AVERAGE TIME TO CREATE PUBLIC KEY : {}".format(avg_pub_key_time))
print("AVERAGE TIME TO CREATE SENDER OBJECT : {}".format(avg_sender_time))
print("AVERAGE TIME TO SIGN DATA : {}".format(avg_sign_time))