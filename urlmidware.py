#!/usr/local/bin/python

import threading
import MySQLdb
import dbmanager
import socket
import time
from logger import Logger

class UrlMidWare(threading.Thread):
	def __init__(self, logger, name):
		super(UrlMidWare, self).__init__()
		self.logger = logger
		self.name = name

	def run(self):
		dbCon = dbmanager.open_db_con()
		dbCur = dbCon.cursor()

		address = ('127.0.0.1', 7030)
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		while True:
			count = dbCur.execute('select uid,url from weburl')
			if count:
				datas = dbCur.fetchall()
				for data in datas:
					msg = 'url,' + data[1]
					s.sendto(msg, address)
					self.logger.logger('WebUrl [%s]' % data[1])
					dbCur.execute('delete from weburl where uid=%s' % data[0])
					dbCon.commit()

			time.sleep(10)	
