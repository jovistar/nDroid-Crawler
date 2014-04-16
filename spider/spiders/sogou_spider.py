from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log
from spider.items import TestItem

class SogouSpider(BaseSpider):
	name = "sogou_spider"
	allowed_domains = ["app.sogou.com"]

	def __init__(self, start=None, stop=None, *args, **kwargs):
		super(SogouSpider, self).__init__(*args, **kwargs)
		self.start_urls = []
		startPage = int(start)
		stopPage = int(stop)
		while startPage != stopPage:
			self.start_urls.append( "http://app.sogou.com/soft/%d/0/1" % startPage )
			startPage = startPage + 1

	def parse(self,response):
		sel = Selector(response)
		for url in sel.xpath('//dl[@class="cf"]/dd/h3/a/@href').extract():
			yield Request('http://app.sogou.com' + url, callback=self.parse)

		for url in sel.xpath('//a[@class="down_pc_btn2"]/@href').extract():
			item = TestItem()
			item['market'] = 'sogou'
			item['url'] = url
			yield item
