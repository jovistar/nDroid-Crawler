from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy import log
from spider.items import TestItem

class AnzhiSpider(BaseSpider):
	name = "anzhi_spider"
	allowed_domains = ["www.anzhi.com"]

	def __init__(self, start=None, stop=None, *args, **kwargs):
		super(AnzhiSpider, self).__init__(*args, **kwargs)
		self.start_urls = []
		startPage = int(start)
		stopPage = int(stop)

		if startPage > stopPage:
			startPage = stopPage

		while startPage != stopPage:
			self.start_urls.append( "http://www.anzhi.com/list_1_%d_hot.html" % startPage)
			startPage = startPage + 1

	def parse(self,response):
		sel = Selector(response)
		for url in sel.xpath('//div[@class="app_down"]/a[@href="javascript:void(0)"]/@onclick').extract():
			item = TestItem()
			item['market'] = 'anzhi'
			item['url'] = 'http://www.anzhi.com/dl_app.php?s=%s&n=5' % url[9:-1]
			yield item
