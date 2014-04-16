#!/usr/bin/python

import threading
import time
import os
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
		while True:
			for spider in self.spiderIns:
				time.sleep(10)
				self.logger.logger('Starting [%s]' % spider)
				os.system('scrapy crawl %s -a start=%d -a stop=%d > /dev/null 2>&1' % ( spider, self.spiderCnfs[spider]['startPage'], self.spiderCnfs[spider]['stopPage']))

			time.sleep(60*60*24*30)
