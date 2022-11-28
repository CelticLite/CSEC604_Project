## System Preferences 
class preferences(args): 
	def __init__(self,args):
		self.args = args
		
	def update(obj):
		length = len(args)



	if args[1] == "PREFERENCES":
	## Change system preferences during runtime

		## Falcon Settings
		if args[2] == "falcon":
			## Setting the value of n for secret key generation. Valid values: 128, 256, 512, 1024
			if args[3] == "secret_n":
				if args[4] == '128':
					obj.n = 128
					obj.logger.warning("n changed to {}. FALCON-{} is not secure".format(obj.n,obj.n))
				elif args[4] == '256':
					obj.n = 256
					obj.logger.warning("n changed to {}. FALCON-{} is not secure".format(obj.n,obj.n))
				elif args[4] == '512':
					obj.n = 512
					obj.logger.info("n changed to {}".format(obj.n))
				elif args[4] == '1024':
					obj.n = 1024
					obj.logger.info("n changed to {}".format(obj.n))
				else:
					raise("ERROR : Invalid value {}".format(str(sys.argv[4])))
			else:
				raise("ERROR : Invalid object {}".format(str(sys.argv[3])))

           	## other settings
		else:
			raise("ERROR : Invalid group {}".format(str(sys.argv[2])))
	else:
		raise("ERROR : Invalid command {}".format(str(sys.argv)))