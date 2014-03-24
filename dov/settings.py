# Scrapy settings for test project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'dov'

SPIDER_MODULES = ['dov.spiders']
NEWSPIDER_MODULE = 'dov.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'test (+http://www.yourdomain.com)'
ITEM_PIPELINES = [
		'dov.pipelines.AppPipeLine'
		]
