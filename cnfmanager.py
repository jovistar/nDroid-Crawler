#!/usr/bin/python

import ConfigParser
import os

class CnfManager():
	def load(self, cnfFile):
		if not os.path.isfile(cnfFile):
			cnfFile = './ndc.cnf'

		cf = ConfigParser.ConfigParser()
		cf.read(cnfFile)

		self.cnfData = {}
		self.cnfData['dirWorking'] = cf.get('dir', 'working')
		self.cnfData['dirStore'] = cf.get('dir', 'store')
		self.cnfData['rpcPort'] = int(cf.get('rpc', 'port'))
		self.cnfData['rpcAuth'] = cf.get('rpc', 'auth')
		self.cnfData['receiverPort'] = int(cf.get('receiver', 'port'))
		self.cnfData['dbHost'] = cf.get('db', 'host')
		self.cnfData['dbUser'] = cf.get('db', 'user')
		self.cnfData['dbPass'] = cf.get('db', 'pass')
		self.cnfData['dbName'] = cf.get('db', 'name')
		self.cnfData['ndlComHost'] = cf.get('ndlcom', 'host')
		self.cnfData['ndlComPort'] = int(cf.get('ndlcom', 'port'))

		self.cnfData['spiders'] = cf.get('spiders', 'spiders').split(',')
		self.cnfData['spiderCnfs'] = {}
		for spider in self.cnfData['spiders']:
			self.cnfData['spiderCnfs'][spider] = {}
			self.cnfData['spiderCnfs'][spider]['pnpc'] = int(cf.get(spider, 'pnpc'))

	def getCnfData(self):
		return self.cnfData
