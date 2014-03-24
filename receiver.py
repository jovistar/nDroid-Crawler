#!/usr/bin/python

import threading
import socket
from Queue import Queue
from logger import Logger
from rpcmonitor import RpcMonitor

class Receiver(threading.Thread):
	def __init__(self, logger, rpcMonitor, rpQueue, name):
		super(Receiver, self).__init__()
		self.logger = logger
		self.rpcMonitor = rpcMonitor
		self.rpQueue = rpQueue
		self.name = name

	def run(self):
		address = ('', 7030)
		udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		udpSocket.bind(address)

		self.rpcMonitor.setCrawleTotal(0)
		while True:
			data,addr = udpSocket.recvfrom(2048)
			self.rpQueue.put(data, 1)
			self.rpcMonitor.incCrawleTotal()
			self.logger.logger('Received [%s]' % data)

		udpSocket.close()

