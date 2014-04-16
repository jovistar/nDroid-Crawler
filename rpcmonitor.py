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
			
			msg = self.buildRspData(initData)
			udpSocket.sendto(msg, addr)
			

		udpSocket.close()

	def buildRspData(self, initData):
		sep = '|'
		rspData = initData + sep + self.startTime + sep + self.mode + sep + '%d' % self.dlThreadNum + sep + '%d' % self.botTotal + sep \
				+ '%d' % self.crawleTotal + sep + '%d' % self.downloadTotal + sep + '%d' % self.pdQueueSize + sep + '%d' % self.downloadedTotal + sep \
				+ '%d' % self.duplicatedTotal + sep + '%d' % self.downloadingTotal

		return rspData

	def setGlobalInfo(self, startTime, mode, dlThreadNum):
		self.startTime = startTime
		self.mode = mode
		self.dlThreadNum = dlThreadNum

	def setCrawleTotal(self, val):
		self.crawleTotal = val

	def incCrawleTotal(self):
		self.crawleTotal = self.crawleTotal + 1

	def setDownloadTotal(self, val):
		self.downloadTotal = val

	def incDownloadTotal(self):
		self.downloadTotal = self.downloadTotal + 1

	def setPdQueueSize(self, val):
		self.pdQueueSize = val

	def incPdQueueSize(self):
		self.pdQueueSize = self.pdQueueSize + 1

	def decPdQueueSize(self):
		self.pdQueueSize = self.pdQueueSize - 1

	def setBotTotal(self, val):
		self.botTotal = val

	def incBotTotal(self):
		self.botTotal = self.botTotal + 1

	def setBots(self, bots):
		self.bots.append(bots)

	def setDownloadedTotal(self, val):
		self.downloadedTotal = val

	def incDownloadedTotal(self):
		self.downloadedTotal = self.downloadedTotal + 1

	def setDuplicatedTotal(self, val):
		self.duplicatedTotal = val

	def incDuplicatedTotal(self):
		self.duplicatedTotal = self.duplicatedTotal + 1

	def setDownloadingTotal(self, val):
		self.downloadingTotal = val

	def incDownloadingTotal(self):
		self.downloadingTotal = self.downloadingTotal + 1

	def decDownloadingTotal(self):
		self.downloadingTotal = self.downloadingTotal - 1
