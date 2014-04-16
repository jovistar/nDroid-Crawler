from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy import log
from dov.items import TestItem

class GfanSpider(BaseSpider):
	name = "gfan_spider"
	allowed_domains = ["apk.gfan.com"]

	#cal
	start_page = 1
	stop_page = ( 1 + 10 )
	start_urls = []
	while start_page != stop_page:
		start_urls.append( "http://apk.gfan.com/apps_7_1_%d.html" % start_page )
		start_page = start_page + 1


	def parse(self,response):
		sel = Selector(response)
		for url in sel.xpath('//li[@class="app-down"]/a/@href').extract():
			item = TestItem()
			item['store'] = 'gfan'
			item['url'] = url
			yield item
