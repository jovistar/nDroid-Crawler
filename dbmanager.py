#!/usr/local/bin/python

import MySQLdb
import ConfigParser
import os
import sys

def open_db_con():
	cf = ConfigParser.ConfigParser()
	cf.read('ncd.cnf')

	db_host = cf.get('db', 'db_host')
	db_user = cf.get('db', 'db_user')
	db_pass = cf.get('db', 'db_pass')
	db_name = cf.get('db', 'db_name')
	
	dbCon = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name, charset='utf8')
	return dbCon

def create_db():
	cf = ConfigParser.ConfigParser()
	cf.read('ncd.cnf')

	db_host = cf.get('db', 'db_host')
	db_user = cf.get('db', 'db_user')
	db_pass = cf.get('db', 'db_pass')
	db_name = cf.get('db', 'db_name')

	dbCon = MySQLdb.connect(host=db_host, user=db_user, passwd=db_pass, charset="utf8")
	cursor = dbCon.cursor()
	cursor.execute('CREATE DATABASE IF NOT EXISTS %s' % db_name)
	cursor.select_db(db_name)




