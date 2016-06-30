import scrapy
from scrapy import Spider
from scrapy.selector import Selector

# defined fields
from hk591.items import Hk591Item

class Hk591Spider(Spider):
	name = "hk591"
	allowed_domains = ['591.com.hk']
	base_url = "http://www.591.com.hk/home/index/deal?t=default&p="
	start_urls = [ base_url+str(i) for i in range(1,564) ]

	def parse(self, response):
		# questions = Selector(response).xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "question-hyperlink", " " ))]')
		deals = response.css('.ft-lt a~ a+ a')
		for deal in deals:
			dealItem = Hk591Item()
			dealItem['name'] = deal.xpath('./text()').extract_first()
			dealItem['url'] = deal.xpath('@href').extract_first()
			yield scrapy.Request(dealItem['url'], meta={'dealItem': dealItem}, callback=self.parse_details)

	def parse_details(self, response):
		dealItem = response.meta['dealItem']
		dealItem['price'] = response.xpath('//*[(@id = "attr")]//em').xpath('./text()').extract_first()
		dealItem['address'] = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "lable", " " ))][text()[contains(.,"Address")]]/following-sibling::*/text()').extract_first()
		yield dealItem