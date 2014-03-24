#!/usr/local/bin/python

import socket
import getopt
import sys
import time

def run_rpc(serverAddr, serverPort, refreshInt):
	address = (serverAddr, serverPort)
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	authCode = 'feu547fn'
	sep = '|'
	while True:
		s.sendto(authCode, address)

		data, addr = s.recvfrom(2048)

		datas = data.split(sep)
		print '**************Ncd Cli Begin*****************'
		print 'Authcode         ' + datas[0]
		print 'Start Time       ' + datas[1]
		print 'Mode             ' + datas[2]
		print 'DL Thread Num    ' + datas[3]
		print 'Bot Total        ' + datas[4]
		print 'Crawle Total     ' + datas[5]
		print 'DL Total         ' + datas[6]
		print 'DL Queue Total   ' + datas[7]
		print 'DLed Total       ' + datas[8]
		print 'DLed Dup Total   ' + datas[9]
		print 'DLing Total      ' + datas[10]
		print '***************Ncd Cli End******************'

		time.sleep(refreshInt)

	s.close()


if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], 'd:p:i:')

	serverAddr = '127.0.0.1'
	serverPort = 7029
	refreshInt = 10
	
	for opt, arg in opts:
		if opt in ('-d'):
			serverAddr = arg
		if opt in ('-p'):
			serverPort = int(arg)
		if opt in ('-i'):
			refreshInt = int(arg)

	run_rpc(serverAddr, serverPort, refreshInt)
