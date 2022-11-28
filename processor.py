##This is where we will define all the definitions used for the processor
from falcon.falcon import PublicKey, SecretKey 

class processor():
	sk = SecretKey(512)
	key = PublicKey(sk)

	def __init__(self,key):
		self.key = key

	def _process_data(data):
		### Find average of numbers in data[]
		print(data)
		average = 0
		_sum = sum(data) 
		print(_sum)
		average = _sum / len(data)
		print(average)
		return average

	def _verify_signature(self,data,sig):
		## Use the public key to verify the data sent 
		return self.key.verify(data,sig)



