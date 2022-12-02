## This is where we will define all the definitions used for the sender
from falcon.falcon import PublicKey, SecretKey 
import logging
import socket

# Setting up Logging 
logging.basicConfig(filename="sender_runtime.log",
                    format='%(levelname)s:%(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


NUMBER_OF_HOSTS = 1  ### This will be dynamically determined 

class sender:
	private_key = SecretKey(512)
	public_key = PublicKey(private_key)
	port = 5500
	
	def __init__(self,pubKey,prvKey):
		self.private_key = prvKey
		self.public_key = pubKey

	def _share_pub_key(self,num_hosts):
		# Share personal public key with all the remote hosts
		server_side = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_side.bind(('',self.port))
		logger.info("socket binded to {} to send pubKey".format(str(self.port)))
		while num_shared < num_hosts:
			c, addr = server_side.accept()    
			logger.info("Got connection from {}".format(str(addr)))
			len_sent = c.send(public_key)
			if len_sent == len(public_key):
				logger.info("Shared public key with {}".format(str(addr)))
				c.close()
			else:
				logger.error("Failed to send public key to {}".format(str(addr)))
				c.close()
			num_shared += 1
	
	def _sign(self,data):
		# sign the data 
		s = self.private_key.sign(data)
		return s

	def _send(self,data,num_hosts,port):
		# Send pre-porcessed data
		client_count = 0 
		print("Welcome to this simple data transfer tool")
		server_side = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			server_side.bind(('',port))
			print(port)
			logger.info("socket binded to {}".format(str(port)))
		except OSError as err:
			try:
				port += random.randrange(500)
				server_side.bind(('',port))
				logger.info("socket binded to {}".format(str(port)))
			except:
				raise(err)
		server_side.listen(num_hosts)
		while client_count < num_hosts:
			c, addr = server_side.accept()    
			logger.info("Got connection from {}".format(str(addr)))
			sig = self._sign(bytes(data[client_count]))	  		
			len_data_sent = c.send(bytes(data[client_count]))
			len_sig_sent = c.send(sig)
			if len_data_sent == len(bytes(data[client_count])) and len_sig_sent == len(sig):
				c.close()
			else:
				len_data_sent_2 = c.send(bytes(data[client_count]))
				len_sig_sent_2 = c.send(sig)
				if len_data_sent_2 == len(bytes(data_to_send)) and len_sig_sent_2 == len(sig):
					c.close()
					logger.info("Sent {} to {}".format(str(data[client_count]),str(addr)))
				else:
					logger.error("Failed to send {} to {}".format(str(data),str(addr)))
					break
			client_count += 1



