#!/usr/bin/python

import threading
import time
import os
from logger import Logger
from rpcmonitor import RpcMonitor

class BotScheduler(threading.Thread):
	def __init__(self, logger, rpcMonitor, name):
		super(BotScheduler, self).__init__()
		self.logger = logger
		self.rpcMonitor = rpcMonitor
		self.name = name

		self.rpcMonitor.setBotTotal(0)
		#scan available spider
		self.logger.logger('Scaning Spiders')
		self.spiders = []
		spiderDir = os.walk('spider/spiders')
		for root, dirs, files in spiderDir:
			for file in files:
				if file == '__init__.py':
					continue
				if file[-3:] == '.py':
					self.spiders.append(file[0:-3])
					self.logger.logger('Found Spider %s' % file[0:-3])
					self.rpcMonitor.incBotTotal()

		self.rpcMonitor.setBots(self.spiders)

	def run(self):
		while True:
			for spider in self.spiders:
				time.sleep(10)
				self.logger.logger('Starting [%s]' % spider)
				os.system('scrapy crawl %s > /dev/null 2>&1' % spider)

			time.sleep(60*60*24*30)
