#!/usr/bin/python

import threading
from Queue import Queue
import pycurl
import hashlib
import time
import os
from logger import Logger
from rpcmonitor import RpcMonitor
import ndutil

class DownloadThread(threading.Thread):
	def __init__(self, args, name):
		super(DownloadThread, self).__init__()
		self.ddQueue = args[0]
		self.dpQueue = args[1]
		self.ddLock = args[2]
		self.pdLock = args[3]
		self.pdQueue = args[4]
		self.logger = args[5]
		self.rpcMonitor = args[6]
		self.name = name

	def run(self):
		curlHandle = pycurl.Curl()
		curlHandle.setopt(pycurl.FOLLOWLOCATION, 1)
		curlHandle.setopt(pycurl.MAXREDIRS, 5)
		curlHandle.setopt(pycurl.CONNECTTIMEOUT, 60)
		curlHandle.setopt(pycurl.TIMEOUT, 300)
		curlHandle.setopt(pycurl.NOSIGNAL, 1)
		while True:
			data, fileName = self.ddQueue.get(1)

			self.rpcMonitor.incDownloadingTotal()
			result = self.download(curlHandle, data, fileName)
			self.rpcMonitor.decDownloadingTotal()
			if result:
				os.remove(fileName)
				self.pdLock.acquire()
				self.pdQueue.put(data, 1)
				self.rpcMonitor.incPdQueueSize()
				self.pdLock.release()
				time.sleep(10)
				continue
			self.ddLock.acquire()
			self.dpQueue.put([data, fileName], 1)
			self.ddLock.release()

			time.sleep(30)

		curlHandle.close()
		
	def download(self, curlHandle, data, fileName):
		file = open(fileName, 'wb')
		curlHandle.setopt(pycurl.WRITEDATA, file)
		curlHandle.setopt(pycurl.URL, data)

		try:
			self.logger.logger('Downloading %s' % data)
			curlHandle.perform()
			file.close()

		except:
			return 1

		return 0

class Downloader(threading.Thread):
	def __init__(self, args, name):
		super(Downloader, self).__init__()
		self.logger = args[0]
		self.rpcMonitor = args[1]
		self.pdQueue = args[2]
		self.dpQueue = args[3]
		self.pdLock = args[4]
		self.dlThreadNum = args[5]
		self.dirWorking = args[6]
		self.name = name

	def run(self):
		numThreads = self.dlThreadNum

		ddLock = threading.Lock()
		downloadThreads = []
		ddQueues = []

		self.rpcMonitor.setDownloadingTotal(0)
		for i in range(numThreads):
			ddQueue = Queue()
			thread = DownloadThread([ddQueue, self.dpQueue, ddLock, self.pdLock, self.pdQueue, self.logger, self.rpcMonitor], 'DownloadThread%s' % i)
			ddQueues.append(ddQueue)
			downloadThreads.append(thread)

		for i in range(numThreads):
			downloadThreads[i].start()

		while True:
			data = self.pdQueue.get(1)

			#generate name
			fileName = '%s/%s.apk' % (self.dirWorking, ndutil.getMd5ByStr(data))

			#select thread
			minQueueIdx = 0
			minQueueSize = ddQueues[minQueueIdx].qsize()
			for i in range(minQueueIdx + 1, numThreads):
				if ddQueues[i].qsize() < minQueueSize:
					minQueueIdx = i
					minQueueSize = ddQueues[i].qsize()

			ddQueues[minQueueIdx].put([data, fileName], 1)

		for i in range(numThreads):
			downloadThreads[i].join()
