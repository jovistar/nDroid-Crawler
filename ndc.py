#!/usr/bin/python

from botscheduler import BotScheduler
from receiver import Receiver
from preprocessor import PreProcessor
from downloader import Downloader
from processor import Processor
from dbmanager import DbManager
from logger import Logger
from rpcmonitor import RpcMonitor
from cnfmanager import CnfManager

import ndutil

from Queue import Queue
import threading
import os
import MySQLdb
import getopt
import sys
from datetime import *
import time

def ncd_loop(doInit, dlThreadNum):
	ndutil.setTimezone()

#read config
	cnfManager = CnfManager()
	cnfManager.load('./ndc.cnf')
	cnfData = cnfManager.getCnfData()

#check dirs
	ndutil.enableDir(cnfData['dirWorking'])
	ndutil.enableDir(cnfData['dirStore'])

#ndlcom
	logger = Logger('nDroid-Crawler', cnfData['ndlComHost'], cnfData['ndlComPort'])
	logger.logger('Initiating')

	dbManager = DbManager(cnfData['dbHost'], cnfData['dbUser'], cnfData['dbPass'], cnfData['dbName'])
	if doInit:
		dbManager.create_table()
		os.system('rm -f %s/*' % cnfData['dirWorking'])
		os.system('rm -f %s/*' % cnfData['dirStore'])

	#logger.logger('Customizing Spiders')
	#spiderGenerator = SpiderGenerator('template', 'spider/spiders')
	#for spider in cnfData['spiders']:
	#	spiderGenerator.gen_spider(spider, cnfData[spider]['startPage'], cnfData[spider]['stopPage'])

	rpQueue = Queue()
	pdQueue = Queue()
	dpQueue = Queue()
	pdLock = threading.Lock()

	rpcMonitor = RpcMonitor(logger, cnfData['rpcPort'], cnfData['rpcAuth'], 'RpcMonitor')
	rpcMonitor.setGlobalInfo(ndutil.getCurrentTimeStr(), 'Standalone', dlThreadNum)
	rpcMonitor.setDownloadTotal(pdQueue.qsize())
	rpcMonitor.setPdQueueSize(pdQueue.qsize())
	
	botScheduler = BotScheduler(logger, rpcMonitor, cnfData['spiders'], cnfData['spiderCnfs'], 'BotScheduler')
	receiver = Receiver(logger, rpcMonitor, rpQueue, cnfData['receiverPort'], 'Receiver')
	preProcessor = PreProcessor(logger, rpcMonitor, rpQueue, pdQueue, pdLock, dbManager, 'PreProcessor')
	downloader = Downloader([logger, rpcMonitor, pdQueue, dpQueue, pdLock, dlThreadNum, cnfData['dirWorking']], 'Downloader')
	processor = Processor(logger, rpcMonitor, dpQueue, pdLock, pdQueue, dbManager, cnfData['dirWorking'], cnfData['dirStore'], 'Processor')

	logger.logger('Starting Threads')
	rpcMonitor.start()
	botScheduler.start()
	receiver.start()
	preProcessor.start()
	downloader.start()
	processor.start()
	
	processor.join()
	downloader.join()
	preProcessor.join()
	receiver.join()
	botScheduler.join()
	rpcMonitor.join()

if __name__ == "__main__":
	opts, args = getopt.getopt(sys.argv[1:], 'it:')

	doInit = False
	dlThreadNum = 5

	for opt, arg in opts:
		if opt in ('-i'):
			doInit = True
		if opt in ('-t'):
			dlThreadNum = int(arg)

	ncd_loop(doInit, dlThreadNum)
