from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy import log
from spider.items import TestItem

class SogouSpider(BaseSpider):
	name = "sogou_spider"
	allowed_domains = ["app.sogou.com"]

	#cal
	start_page = ($s1$)
	stop_page = ($s2$)
	start_urls = []
	while start_page != stop_page:
		start_urls.append( "http://app.sogou.com/soft/%d/0/1" % start_page )
		start_page = start_page + 1


	def parse(self,response):
		sel = Selector(response)
		for url in sel.xpath('//div[@class="item1"]/a/@href').extract():
			item = TestItem()
			item['market'] = 'sogou'
			item['url'] = url
			yield item
