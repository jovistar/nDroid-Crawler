#!/usr/bin/python

import threading
from Queue import Queue
import hashlib
import os
import shutil
from logger import Logger
from rpcmonitor import RpcMonitor
from dbmanager import DbManager
import ndutil

class Processor(threading.Thread):
	def __init__(self, logger, rpcMonitor, dpQueue, pdLock, pdQueue, dbManager, dirWorking, dirStore, name):
		super(Processor, self).__init__()
		self.logger = logger
		self.rpcMonitor = rpcMonitor
		self.dpQueue = dpQueue
		self.pdLock = pdLock
		self.pdQueue = pdQueue
		self.dbManager = dbManager
		self.dirWorking = dirWorking
		self.dirStore = dirStore
		self.name = name

	def run(self):
		self.rpcMonitor.setDownloadedTotal(0)
		self.rpcMonitor.setDuplicatedTotal(0)
		while True:
			data, fileName = self.dpQueue.get(1)
			self.rpcMonitor.decPdQueueSize()

			#filte 0KB file
			if ndutil.getSize(fileName) == 0:
				self.pdLock.acquire()
				self.pdQueue.put(data, 1)
				self.rpcMonitor.incPdQueueSize()
				self.pdLock.release()
				continue

			#duplicate?
			md5Value = ndutil.getMd5(fileName)

			path = self.dbManager.get_path_by_hashval(md5Value)
			if path is not None:
				self.dbManager.update_item(data, 'NULL', path, md5Value, 1)
				self.rpcMonitor.incDuplicatedTotal()
				self.logger.logger('Duplicated %s' % path)
				os.remove(fileName)
				continue

			newFileName = '%s/%s.apk' % (self.dirStore, md5Value)
			shutil.move(fileName, newFileName)
			self.dbManager.update_item(data, 'NULL', newFileName, md5Value, 1)
			self.rpcMonitor.incDownloadedTotal()
			self.logger.logger('Downloaded %s' % data)
