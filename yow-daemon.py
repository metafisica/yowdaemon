#!/usr/bin/env python

import sys,time,os
from daemon 				import Daemon
from layer				import DaemonLayer
from yowsup.layers.auth                 import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_messages    import YowMessagesProtocolLayer
from yowsup.layers.protocol_receipts    import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks        import YowAckProtocolLayer
from yowsup.layers.network              import YowNetworkLayer
from yowsup.layers.coder                import YowCoderLayer
from yowsup.stacks                      import YowStack
from yowsup.common                      import YowConstants
from yowsup.layers                      import YowLayerEvent
from yowsup.stacks                      import YowStack, YOWSUP_CORE_LAYERS
from yowsup 				import env
import subprocess
import logging
logging.basicConfig(level=logging.ERROR)

class YowsupDaemon(Daemon):
	def run(self):
		mess=None
		to=None
		with open(appPath+'/config.cfg') as f:
			for line in f:
				if line.find('phone number:',0)==0:
                                        phone=line[13:]
                                        phone=phone.strip()
                                elif line.find('password:',0)==0:
                                        passw=line[9:].strip()
				elif line.find('send_message_startup:',0)==0:
					mess=line[21:-1]
					mess= '\'' + mess + '\''
				elif line.find('allowed1:',0)==0:
					to=line[9:-1]
                CREDENTIALS = (phone, passw)
		print '/send.py '+to+' '+mess
		p=subprocess.Popen(appPath+'/send.py '+to+' '+mess,stdout=subprocess.PIPE, shell=True)
		(output,err)=p.communicate()
		while True: 
	                layers = (
	                            DaemonLayer,
	                            (YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer,YowAckProtocolLayer)
	                            ) + YOWSUP_CORE_LAYERS
	
	                stack = YowStack(layers)
	                stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, CREDENTIALS)
	                stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])
	                stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)   
	                stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())
	                stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
			interface=stack.getLayer(6)
			interface.initialize(appPath)
			try:
				stack.loop()
			except:
				pass

if __name__== '__main__':
	daemon = YowsupDaemon('/tmp/yowsup-daemon.pid',True)
	appPath=os.getcwd()
	usage='Use %s help\n'   %sys.argv[0]
	if len(sys.argv)==2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'status' == sys.argv[1]:
			daemon.status()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'undaemon' == sys.argv[1]:
			daemon.nodaemon()
		elif 'help' == sys.argv[1]:
			with open(appPath+'/Instructions') as f:
				for line in f:
					print line[0:-1]
		elif 'about' == sys.argv[1]:
			print 'Yow-daemon, yowsup based remote control,\n'\
				'Tread Soft 2015 tweeter: @treadsoftblog'
		elif 'license' ==sys.argv[1]:
			with open(appPath+'/LICENSE') as f:
				for line in f:
					print line			
		else:
			print usage
			sys.exit(2)
		sys.exit(0)
	else:
		print usage	
		sys.exit(2)
