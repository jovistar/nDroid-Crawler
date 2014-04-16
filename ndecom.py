#!/usr/bin/python

import socket
import json
import os

class NdeCom():
	def __init__(self, host, port):
		self.address = (host, port)
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def create(self, path):
		data = {}
		data['request'] = 'create'
		
		if not os.path.isfile(path):
			return 1
		data['path'] = os.path.abspath(path)

		result = self.doCom(data)
		if result['response'] != 0:
			return 1 
		else:
			return 0

	def doCom(self, data):
		msg = json.dumps(data)
		self.s.sendto(msg, self.address)
		result,addr = self.s.recvfrom(4096)

		return json.loads(result)
