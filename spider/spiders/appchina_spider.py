from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log
from spider.items import TestItem

class SogouSpider(BaseSpider):
	name = "appchina_spider"
	allowed_domains = ["www.appchina.com"]

	def __init__(self, start=None, stop=None, *args, **kwargs):
		super(SogouSpider, self).__init__(*args, **kwargs)
		self.start_urls = []

		for i in range(1,16):
			startPage = int(start)
			stopPage = int(stop)
			if startPage > stopPage:
				startPage = stopPage

			while startPage != stopPage:
				self.start_urls.append( "http://www.appchina.com/category/3%02d/1_%d_1_2_0_0_0.html" % (i, startPage) )
				startPage = startPage + 1

	def parse(self,response):
		sel = Selector(response)

		for url in sel.xpath('//div[@id="byrate"]/ul[@class="app_list"]/li/div/a[@class="download_app"]/@href').extract():
			item = TestItem()
			item['market'] = 'appchina'
			item['url'] = url
			yield item
