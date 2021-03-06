#!/usr/bin/python

import threading
import time
import os
import socket
from logger import Logger
from rpcmonitor import RpcMonitor

class BotScheduler(threading.Thread):
	def __init__(self, logger, rpcMonitor, spiders, spiderCnfs, name):
		super(BotScheduler, self).__init__()
		self.logger = logger
		self.rpcMonitor = rpcMonitor
		self.spiders = spiders
		self.spiderCnfs = spiderCnfs
		self.name = name

		self.addr = ('', 7031)
		self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.udpSocket.bind(self.addr)

		self.rpcMonitor.setBotTotal(0)
		#scan available spider
		self.logger.logger('Scaning Spiders')
		self.spiderIns = []
		spiderDir = os.walk('spider/spiders')
		for root, dirs, files in spiderDir:
			for file in files:
				if file == '__init__.py':
					continue
				if file[-3:] == '.py':
					spiderName = file[0:-3]
					if spiderName in self.spiders:
						self.spiderIns.append(spiderName)
						self.logger.logger('Found Spider %s' % spiderName)
						self.rpcMonitor.incBotTotal()

		self.rpcMonitor.setBots(self.spiderIns)

	def run(self):
		cnfs = {}
		for spider in self.spiderIns:
			cnfs[spider] = {}
			cnfs[spider]['start'] = 1
			cnfs[spider]['stop'] = 1 + self.spiderCnfs[spider]['pnpc']

		#wait for all coms
		time.sleep(15)
		data,addr = self.udpSocket.recvfrom(32)
		while True:
			for spider in self.spiderIns:
				if cnfs[spider]['start'] == cnfs[spider]['stop']:
					time.sleep(150)
					continue
				self.logger.logger('Starting %s' % spider)
				#os.system('scrapy crawl %s -a start=%d -a stop=%d' % ( spider, cnfs[spider]['start'], cnfs[spider]['start'] + 1))
				os.system('scrapy crawl %s -a start=%d -a stop=%d > /dev/null 2>&1' % ( spider, cnfs[spider]['start'], cnfs[spider]['start'] + 1))
				cnfs[spider]['start'] = cnfs[spider]['start'] + 1
				
				data,addr = self.udpSocket.recvfrom(32)

		time.sleep(60*60*24*30)
