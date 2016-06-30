from scrapy import Spider
from scrapy.selector import Selector

# defined fields
from stack.items import StackItem

class StackSpider(Spider):
	name = "stack"
	allowed_domains = ['stackoverflow.com']
	start_urls = [
	"http://stackoverflow.com/questions?pagesize=50&sort=newest",
	]

	def parse(self, response):
		questions = Selector(response).xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "question-hyperlink", " " ))]')

		for question in questions:
			item = StackItem()
			item['title'] = question.css('::text').extract_first()
			item['url'] = response.urljoin(questions.css('::attr(href)').extract_first())
			yield item