#!/usr/bin/python

from botscheduler import BotScheduler
from receiver import Receiver
from preprocessor import PreProcessor
from downloader import Downloader
from processor import Processor

from Queue import Queue
import threading
import os
import MySQLdb
import getopt
import sys
from datetime import *
import time

from urlmidware import UrlMidWare
from logger import Logger
from rpcmonitor import RpcMonitor
import dbmanager

def clear_all():
	os.system('rm -f apk/*')
	dbCon = dbmanager.open_db_con()
	dbCur = dbCon.cursor()
	dbCur.execute('delete from crawler')
	dbCon.commit()
	dbCur.close()
	dbCon.close()

def restore_pdqueue(pdQueue):
	dbCon = dbmanager.open_db_con()
	dbCur = dbCon.cursor()
	dbCur.execute('select url from crawler where hashvalue="NULL"')
	
	urls = dbCur.fetchall()
	for url in urls:
		pdQueue.put(str(url[0]), 1)

	dbCur.close()
	dbCon.close()

def ncd_loop(debugMode, logMode, botInterval, dlThreadNum, noSpider):
	os.environ['TZ'] = 'Asia/Shanghai'
	time.tzset()
	curTime = datetime.now()
	startTime = curTime.strftime('%Y-%m-%d %H:%M:%S')

	if not os.path.exists('apk'):
		os.mkdir('apk')
	if not os.path.exists('tmp'):
		os.mkdir('tmp')

	logger = Logger(logMode)
	logger.logger('Initiating')
	os.system('rm -f tmp/*')

	if debugMode:
		logger.logger('Entering DEBUG Mode')
	else:
		logger.logger('Entering NORMAL Mode')

	rpQueue = Queue()
	pdQueue = Queue()
	dpQueue = Queue()
	pdLock = threading.Lock()

	mode = 'NORMAL'
	if debugMode:
		clear_all()
		mode = 'DEBUG'
	else:
		restore_pdqueue(pdQueue)

	logger.logger('Starting Threads')
	rpcMonitor = RpcMonitor(logger, 'RpcMonitor')
	rpcMonitor.setGlobalInfo(startTime, mode, dlThreadNum)
	rpcMonitor.setDownloadTotal(pdQueue.qsize())
	rpcMonitor.setPdQueueSize(pdQueue.qsize())

	
	botScheduler = BotScheduler(logger, rpcMonitor, botInterval, noSpider, 'BotScheduler')
	receiver = Receiver(logger, rpcMonitor, rpQueue, 'Receiver')
	preProcessor = PreProcessor(logger, rpcMonitor, rpQueue, pdQueue, pdLock, 'PreProcessor')
	downloader = Downloader([logger, rpcMonitor, pdQueue, dpQueue, pdLock, dlThreadNum], 'Downloader')
	processor = Processor(logger, rpcMonitor, dpQueue, pdLock, pdQueue, 'Processor')
	urlMidWare = UrlMidWare(logger, 'UrlMidWare')

	rpcMonitor.start()
	botScheduler.start()
	receiver.start()
	preProcessor.start()
	downloader.start()
	processor.start()
	urlMidWare.start()
	
	urlMidWare.join()
	processor.join()
	downloader.join()
	preProcessor.join()
	receiver.join()
	botScheduler.join()
	rpcMonitor.join()

if __name__ == "__main__":
	opts, args = getopt.getopt(sys.argv[1:], 'dvi:t:c')

	debugMode = False
	logMode = 'LOGONLY'
	botInterval = 60*60*24*15
	dlThreadNum = 5
	noSpider = False

	for opt, arg in opts:
		if opt in ('-d'):
			debugMode = True
		if opt in ('-v'):
			logMode = 'LOGPRINT'
		if opt in ('-i'):
			botInterval = int(arg)
		if opt in ('-t'):
			dlThreadNum = int(arg)
		if opt in ('-c'):
			noSpider = True

	ncd_loop(debugMode, logMode, botInterval, dlThreadNum, noSpider)
