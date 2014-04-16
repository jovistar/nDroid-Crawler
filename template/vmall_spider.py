from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy import log
from spider.items import TestItem

class VmallSpider(BaseSpider):
	name = "vmall_spider"
	allowed_domains = ["app.vmall.com"]

	#cal
	start_page = ($s1$)
	stop_page = ($s2$)
	start_urls = []
	while start_page != stop_page:
		start_urls.append( "http://app.vmall.com/soft/list_13_0_%d" % start_page )
		start_page = start_page + 1


	def parse(self,response):
		sel = Selector(response)
		for url in sel.xpath('//li[@class="app-down"]/a/@href').extract():
			item = TestItem()
			item['market'] = 'gfan'
			item['url'] = url
			yield item
