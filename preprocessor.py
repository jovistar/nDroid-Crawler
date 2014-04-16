#!/usr/bin/python

import threading
import MySQLdb
from Queue import Queue
from logger import Logger
from rpcmonitor import RpcMonitor
from dbmanager import DbManager

class PreProcessor(threading.Thread):
	def __init__(self, logger, rpcMonitor, rpQueue, pdQueue, pdLock, dbManager, name):
		super(PreProcessor, self).__init__()
		self.logger = logger
		self.rpcMonitor = rpcMonitor
		self.rpQueue = rpQueue
		self.pdQueue = pdQueue
		self.pdLock = pdLock
		self.dbManager = dbManager
		self.name = name

	def run(self):
		while True:
			tmp = self.rpQueue.get(1)
			data = tmp.split(',', 1)

			if self.dbManager.item_exists(data[1], data[0]):
				continue

			self.dbManager.insert_item(data[1], data[0], 'NULL', 'NULL', 0)
			self.rpcMonitor.incDownloadTotal()
			self.logger.logger('Inserted %s' % data)
			self.pdLock.acquire()
			self.pdQueue.put(data[1], 1)
			self.rpcMonitor.incPdQueueSize()
			self.pdLock.release()
