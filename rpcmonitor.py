#!/usr/local/bin/python

import threading
import socket
from logger import Logger


class RpcMonitor(threading.Thread):
	def __init__(self, logger, port, auth, name):
		super(RpcMonitor, self).__init__()
		self.logger = logger
		self.name = name
		self.port = port
		self.auth = auth

		self.lock = threading.Lock()
		self.botTotal = 0
		self.bots = []
		self.crawleTotal = 0
		self.downloadTotal = 0
		self.pdQueueSize = 0
		self.downloadedTotal = 0
		self.duplicatedTotal = 0
		self.downloadingTotal = 0

	def run(self):
		address = ('', self.port)
		udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		udpSocket.bind(address)

		while True:
			data, addr = udpSocket.recvfrom(1024)
			if data != self.auth:
				self.logger.logger('Unauthorized RPC Request')
				continue

			self.logger.logger('Authorized RPC Request')
			
			msg = self.buildRspData(data)
			udpSocket.sendto(msg, addr)
			

		udpSocket.close()

	def buildRspData(self, initData):
		sep = '|'
		rspData = initData + sep + self.startTime + sep + self.mode + sep + '%d' % self.dlThreadNum + sep + '%d' % self.botTotal + sep \
				+ '%d' % self.crawleTotal + sep + '%d' % self.downloadTotal + sep + '%d' % self.pdQueueSize + sep + '%d' % self.downloadedTotal + sep \
				+ '%d' % self.duplicatedTotal + sep + '%d' % self.downloadingTotal

		return rspData

	def setGlobalInfo(self, startTime, mode, dlThreadNum):
		self.lock.acquire()
		self.startTime = startTime
		self.mode = mode
		self.dlThreadNum = dlThreadNum
		self.lock.release()

	def setCrawleTotal(self, val):
		self.lock.acquire()
		self.crawleTotal = val
		self.lock.release()

	def incCrawleTotal(self):
		self.lock.acquire()
		self.crawleTotal = self.crawleTotal + 1
		self.lock.release()

	def setDownloadTotal(self, val):
		self.lock.acquire()
		self.downloadTotal = val
		self.lock.release()

	def incDownloadTotal(self):
		self.lock.acquire()
		self.downloadTotal = self.downloadTotal + 1
		self.lock.release()

	def setPdQueueSize(self, val):
		self.lock.acquire()
		self.pdQueueSize = val
		self.lock.release()

	def incPdQueueSize(self):
		self.lock.acquire()
		self.pdQueueSize = self.pdQueueSize + 1
		self.lock.release()

	def decPdQueueSize(self):
		self.lock.acquire()
		self.pdQueueSize = self.pdQueueSize - 1
		self.lock.release()

	def setBotTotal(self, val):
		self.lock.acquire()
		self.botTotal = val
		self.lock.release()

	def incBotTotal(self):
		self.lock.acquire()
		self.botTotal = self.botTotal + 1
		self.lock.release()

	def setBots(self, bots):
		self.lock.acquire()
		self.bots.append(bots)
		self.lock.release()

	def setDownloadedTotal(self, val):
		self.lock.acquire()
		self.downloadedTotal = val
		self.lock.release()

	def incDownloadedTotal(self):
		self.lock.acquire()
		self.downloadedTotal = self.downloadedTotal + 1
		self.lock.release()

	def setDuplicatedTotal(self, val):
		self.lock.acquire()
		self.duplicatedTotal = val
		self.lock.release()

	def incDuplicatedTotal(self):
		self.lock.acquire()
		self.duplicatedTotal = self.duplicatedTotal + 1
		self.lock.release()

	def setDownloadingTotal(self, val):
		self.lock.acquire()
		self.downloadingTotal = val
		self.lock.release()

	def incDownloadingTotal(self):
		self.lock.acquire()
		self.downloadingTotal = self.downloadingTotal + 1
		self.lock.release()

	def decDownloadingTotal(self):
		self.lock.acquire()
		self.downloadingTotal = self.downloadingTotal - 1
		self.lock.release()
