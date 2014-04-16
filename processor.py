#!/usr/bin/python

import threading
import MySQLdb
from Queue import Queue
import hashlib
import os
import shutil
from logger import Logger
import dbmanager
from rpcmonitor import RpcMonitor
import ndutil
from ndecom import NdeCom

class Processor(threading.Thread):
	def __init__(self, logger, rpcMonitor, dpQueue, pdLock, pdQueue, name):
		super(Processor, self).__init__()
		self.logger = logger
		self.rpcMonitor = rpcMonitor
		self.dpQueue = dpQueue
		self.pdLock = pdLock
		self.pdQueue = pdQueue
		self.name = name
		self.ndeCom = NdeCom('127.0.0.1', 12325)

	def run(self):
		dbCon = dbmanager.open_db_con()
		dbCur = dbCon.cursor()

		self.rpcMonitor.setDownloadedTotal(0)
		self.rpcMonitor.setDuplicatedTotal(0)
		while True:
			data, fileName = self.dpQueue.get(1)
			self.rpcMonitor.decPdQueueSize()

			#filte 0KB file
			if os.path.getsize(fileName) == 0:
				self.pdLock.acquire()
				self.pdQueue.put(data, 1)
				self.rpcMonitor.incPdQueueSize()
				self.pdLock.release()
				continue

			#duplicate?
			m = hashlib.md5()
			fileHandle = open(fileName, 'rb')
			m.update(fileHandle.read())
			md5Value = m.hexdigest()
			fileHandle.close()

			count = dbCur.execute('select aid,path from crawler where hashvalue=%s', [md5Value])
			if count:
				aid, path = dbCur.fetchone()
				value = [1, path, md5Value, data]
				dbCur.execute('update crawler set downloaded=%s,path=%s,hashvalue=%s where url=%s', value)
				dbCon.commit()
				self.rpcMonitor.incDuplicatedTotal()
				self.logger.logger('Duplicated [%s]' % path)
				os.remove(fileName)
				continue

			newFileName = 'apk/%s.apk' % md5Value
			shutil.move(fileName, newFileName)
			value = [1, newFileName, md5Value, data]
			dbCur.execute('update crawler set downloaded=%s,path=%s,hashvalue=%s where url=%s', value)
			dbCon.commit()
			self.rpcMonitor.incDownloadedTotal()
			self.logger.logger('Downloaded [%s]' % data)

			path = ndutil.getAbstractPath(newFileName)
			self.ndeCom.create(path)

		dbCur.close()
		dbCon.close()
