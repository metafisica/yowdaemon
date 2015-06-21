#!/usr/bin/env python

from yowsup.demos import sendclient
from yowsup 	import env
import sys,time,os
import logging
logging.basicConfig(level=logging.ERROR)

if len(sys.argv)!=3:
	print 'Usage: %s phone_number message' %sys.argv[0]	
	sys.exit(0)
with open(os.path.dirname(os.path.realpath(sys.argv[0]))+'/config.cfg') as f:
	for line in f:
		if line.find('phone number:',0)==0:
			phone=line[13:]
			phone=phone.strip()
		elif line.find('password:',0)==0:
			passwd=line[9:].strip()
credentials=(phone,passwd)
try:
	stack = sendclient.YowsupSendStack(credentials, [([sys.argv[1], sys.argv[2]])],False)
	stack.start()
except KeyboardInterrupt:
	print 'Message delivered, did it arrive?'
	sys.exit(0)
