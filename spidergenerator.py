#!/jusr/bin/python

import os

class SpiderGenerator():
	def __init__(self, dirTemplate, dirSpiders):
		self.dirTemplate = dirTemplate
		self.dirSpiders = dirSpiders

	def gen_spider(self, market, startPage, stopPage):
		spider = '%s_spider' % market
		spiderFile = spider + '.py'

		templateSpider = self.dirTemplate + '/' + spiderFile
		deploySpider = self.dirSpiders + '/' + spiderFile
		
		fileHandle = open(templateSpider, 'r')
		content = fileHandle.read()
		n1 = content.replace('($s1$)', str(startPage))
		finalContent = n1.replace('($s2$)', str(stopPage))
		fileHandle.close()

		fileHandle = open(deploySpider, 'w')
		fileHandle.write(finalContent)
		fileHandle.close()



