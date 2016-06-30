# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# packages for login forms
from scrapy.http import FormRequest
from loginform import fill_login_form

from ScrapyAfterLoginExample.items import ScrapyafterloginexampleItem


class GithubSpider(CrawlSpider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']

    login_user = 'XXXXXXXXXX'
    login_password = 'XXXXXXXXXX'

    def parse(self, response):
    	# using fill_login_form to perform a login
    	args, url, method = fill_login_form(response.url, response.body, self.login_user, self.login_password)
    	return FormRequest(url, method=method, formdata=args, callback=self.after_login)

    def after_login(self, response):
    	items = response.css('.body .simple')
    	for i in items:
    		name = i.xpath('./div')[0].xpath('./a')[1].xpath('./text()').extract_first()
    		url = response.urljoin(i.xpath('./div')[0].xpath('./a')[1].xpath('./@href').extract_first())
    		yield {
    		'name': name,
    		'url': url
    		}