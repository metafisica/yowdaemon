from yowsup.layers.interface 				import YowInterfaceLayer, ProtocolEntityCallback 
from yowsup.layers.protocol_messages.protocolentities 	import TextMessageProtocolEntity 
from yowsup.layers.protocol_receipts.protocolentities 	import OutgoingReceiptProtocolEntity 
from yowsup.layers.protocol_acks.protocolentities 	import OutgoingAckProtocolEntity 
import subprocess 
import threading
import time
import sys, os 

class DaemonLayer(YowInterfaceLayer):
	dic={}
	allowshell=False
	dictStart=False
	allowed=[]
		
	def initialize(self,path):
		with open(path+'/config.cfg') as f:
			for line in f:
				if line.find('Command dictionary',1)==1:
                                        self.dictStart=True
                                elif line.find('allowed',0,7)==0:
                                        self.allowed.append(line[9:20])
                                elif not line.find('allow_direct_shell',0)==-1:
                                        self.allowshell=True
                                if self.dictStart and not line.find(':',0)==-1:
                                        self.dic[line.split(':',1)[0]]=line.split(':',1)[1]

	@ProtocolEntityCallback("message")
	def onMessage(self, messageProtocolEntity):
		#send receipt otherwise we keep receiving the same message over and over
	        if True:
	            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())
	            self.toLower(receipt)
		    order = messageProtocolEntity.getBody()
		    print 'Message received from: ' +messageProtocolEntity.getFrom()[0:11]
		    print 'On: ' + time.strftime('%d-%m-%Y %H:%M:%S')
		    print order
		    if not messageProtocolEntity.getFrom()[23:24]=='g':
	            	    if messageProtocolEntity.getBody() in self.dic or messageProtocolEntity.getBody()[0:6]=="Shell:":
				    if messageProtocolEntity.getFrom()[0:11] in self.allowed:
					order = messageProtocolEntity.getBody()
					if order[0:6]=="Shell:": 
						if self.allowshell:
								order=order[7:]
						else:
							order="echo No permitido"
					else:
						order=self.dic[order]
					p=subprocess.Popen(order,stdout=subprocess.PIPE,shell=True)
					(output,err)=p.communicate()
					p_status=p.wait()
					order=output[:-1]
				    else:
					order="Lo siento no tienes permiso para ejecutar ordenes."
			    else:
				order='No te he entendido'
				
			    outgoingMessageProtocolEntity=TextMessageProtocolEntity(order,to=messageProtocolEntity.getFrom())     
			    self.toLower(outgoingMessageProtocolEntity)	
		    else:
			    print "group message"	    

	@ProtocolEntityCallback("receipt")
	def onReceipt(self, entity):
		ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", "delivery")
		self.toLower(ack)

	'''
	@ProtocolEntityCallback("ack")
	def onAck (self, entiy):
		self.lock.acquire()
		if entity.getId() in self.ackQueue:
			self.ackQueue.pop(self.ackQueue.index(entity.getId()))

		if not len(self.ackQueue):
			self.lock.release()
			raise KeyboardInterrupt
			
		self.lock.release
	'''
