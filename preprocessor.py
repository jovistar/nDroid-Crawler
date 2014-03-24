#!/usr/bin/python

import threading
import MySQLdb
from Queue import Queue
from logger import Logger
import dbmanager
from rpcmonitor import RpcMonitor

class PreProcessor(threading.Thread):
	def __init__(self, logger, rpcMonitor, rpQueue, pdQueue, pdLock, name):
		super(PreProcessor, self).__init__()
		self.logger = logger
		self.rpcMonitor = rpcMonitor
		self.rpQueue = rpQueue
		self.pdQueue = pdQueue
		self.pdLock = pdLock
		self.name = name

	def run(self):
		dbCon = dbmanager.open_db_con()
		dbCur = dbCon.cursor()

		while True:
			tmp = self.rpQueue.get(1)
			data = tmp.split(',', 1)
			value = [0, data[1], data[0], 0, 'NULL','NULL']

			#duplicate?
			count = dbCur.execute('select aid from crawler where url=%s and store=%s', [value[1], value[2]])
			if count:
				continue

			dbCur.execute('insert into crawler values(%s,%s,%s,%s,%s,%s)', value)
			dbCon.commit()
			self.rpcMonitor.incDownloadTotal()
			self.logger.logger('Inserted [%s]' % value[1])
			self.pdLock.acquire()
			self.pdQueue.put(value[1], 1)
			self.rpcMonitor.incPdQueueSize()
			self.pdLock.release()

		dbCur.close()
		dbCon.close()
