# Test script for verifying signatures
from falcon.falcon import PublicKey, SecretKey 
from processor import processor
from sender import sender
import time 

#valid data and sender 
data = bytearray([3,4,5,6,7,8])
prv_key = SecretKey(512)
pubKey = PublicKey(prv_key)
s = sender(pubKey,prv_key)
sig = s._sign(data)

# invalid key pair
bad_prv_key = SecretKey(512)
bad_key = PublicKey(bad_prv_key)
wrong_p = processor(bad_key)

avg_processor_time = 0 
avg_verify_time = 0 
avg_false_time = 0 
correct = 0
incorrect = 0

for i in range(0,100):
	pro_begin = time.time()
	my_p = processor(pubKey)
	pro_end = time.time()
	print("Processor took {} seconds to init.".format(pro_end - pro_begin))
	avg_processor_time += pro_end - pro_begin

	verify_begin = time.time()
	correct_sig = my_p._verify_signature(data,sig)
	verify_end = time.time()
	print("Signature verification with the correct pub key took {} seconds.".format(verify_end - verify_begin))
	avg_verify_time += verify_end - verify_begin

	if correct_sig:
		print("The signature is valid")
		correct += 1
	else:
		print("The singature is NOT valid")
		incorrect += 1

	wrong_verify_begin = time.time()
	incorrect_sig = wrong_p._verify_signature(data,sig)
	wrong_verify_end = time.time()
	print("Signature verification with the wrong pub key took {} seconds.".format(wrong_verify_end - wrong_verify_begin))
	avg_false_time += wrong_verify_end - wrong_verify_begin

	if incorrect_sig:
		print("The signature is valid")
		incorrect += 1
	else:
		print("The singature is NOT valid")
		correct += 1


avg_processor_time = avg_processor_time / 100.0
avg_verify_time = avg_verify_time / 100.0
avg_false_time = avg_false_time / 100.0

print("AVERAGE TIME TO MAKE PROCESSOR OBJECT: {}".format(avg_processor_time))
print("AVERAGE TIME TO VERIFY SIGNATURE WITH VALID PUBLIC KEY: {}".format(avg_verify_time))
print("AVERAGE TIME TO VERIFY SIGNATURE WITH INVALID PUBLIC KEY: {}".format(avg_false_time))
print("TOTAL NUMBER OF SUCCESSES: {}".format(correct))
print("TOTAL NUMBER OF FAILURES: {}".format(incorrect))