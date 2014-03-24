# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy import log
import socket

class AppPipeLine(object):
	udpSocket = None
	serverAddr = ('127.0.0.1', 7030)

	def __init__(self):
		dispatcher.connect(self.initialize, signals.engine_started)
		dispatcher.connect(self.finalize, signals.engine_stopped)
		
	def process_item(self, item, spider):
		data = item['store'] + ',' + item['url']
		self.udpSocket.sendto(data, self.serverAddr)
		return item

	def initialize(self):
		self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		log.msg("App PipeLine Opened!!!", log.DEBUG)

	def finalize(self):
		self.udpSocket.close()
		log.msg("App PipeLine Closed!!!", log.DEBUG)
