from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy import log
from spider.items import TestItem

class GfanSpider(BaseSpider):
	name = "gfan_spider"
	allowed_domains = ["apk.gfan.com"]

	def __init__(self, start=None, stop=None, *args, **kwargs):
		super(GfanSpider, self).__init__(*args, **kwargs)
		self.start_urls = []
		startPage = int(start)
		stopPage = int(stop)

		if startPage > stopPage:
			startPage = stopPage

		while startPage != stopPage:
			self.start_urls.append( "http://apk.gfan.com/apps_7_1_%d.html" % startPage)
			startPage = startPage + 1

	def parse(self,response):
		sel = Selector(response)
		for url in sel.xpath('//li[@class="app-down"]/a/@href').extract():
			item = TestItem()
			item['market'] = 'gfan'
			item['url'] = url
			yield item
