#!/usr/local/bin/python

import MySQLdb
import threading

class DbManager():
	def __init__(self, dbHost, dbUser, dbPass, dbName):
		self.dbCon = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName, charset='utf8')
		self.dbCursor = self.dbCon.cursor()
		self.lock = threading.Lock()

	def create_table(self):
		self.drop_table()
		self.dbCursor.execute('CREATE TABLE crawler(cid int auto_increment primary key not null,url varchar(2048) not null,market varchar(32) not null,path varchar(2048) not null,hashval varchar(128) not null, download int not null)')
		self.dbCon.commit()

	def drop_table(self):
		self.dbCursor.execute('DROP TABLE IF EXISTS crawler')
		self.dbCon.commit()

	def test_table(self):
		return True

	def clear_table(self):
		self.lock.acquire()
		self.dbCursor.execute('DELETE FROM crawler')
		self.dbCon.commit()
		self.lock.release()

	def item_exists(self, url, market):
		self.lock.acquire()
		count = self.dbCursor.execute('SELECT cid FROM crawler WHERE url=%s AND market=%s', (url, market))
		self.lock.release()
		if count:
			return True
		return False

	def insert_item(self, url, market, path, hashval, download):
		self.lock.acquire()
		self.dbCursor.execute('INSERT INTO crawler values(%s,%s,%s,%s,%s,%s)', (0, url, market, path, hashval, download))
		self.dbCon.commit()
		self.lock.release()

	def update_item(self, url, market, path, hashval, download):
		self.lock.acquire()
		self.dbCursor.execute('UPDATE crawler SET path=%s,hashval=%s,download=%s WHERE url=%s', (path, hashval, download, url))
		self.dbCon.commit()
		self.lock.release()

	def get_path_by_hashval(self, hashVal):
		self.lock.acquire()
		count = self.dbCursor.execute('SELECT path FROM crawler WHERE hashval=%s AND download=1', (hashVal,))
		if count:
			result = self.dbCursor.fetchone()
			self.lock.release()
			return result[0]

		self.lock.release()
		return None


