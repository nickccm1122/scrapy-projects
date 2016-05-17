import scrapy


class Spider(scrapy.Spider):
    name = 'playgrounds'
    # start_urls = ['http://www.591.com.hk/home/index/deal?t=default&p='+str(i) for i in range(1,547)]
    start_urls = ['http://www.lcsd.gov.hk/tc/facilities/facilitieslist/districts.php?ftid=3&fcid=8']

    def parse(self, response):
        for link in response.css('.linkgp_links a'):

            full_url = response.urljoin(link.css('a::attr(href)')[0].extract())
            district = link.css('a::text')[0].extract()

            yield scrapy.Request(full_url, meta={'district': district}, callback=self.parse_district)
            yield scrapy.Request(full_url, callback=self.parse_district)


    def parse_district(self, response):
        for tbody in response.css('table'):
            if response.css('tr:nth-child(1) td+ td::text').extract()> 0:
                pitch_name = response.css('tr:nth-child(1) td+ td::text').extract()[0].encode('utf8')
            else:
                pitch_name = response.css('tr:nth-child(1) td+ td::text').extract().encode('utf8')

            if response.css('tr:nth-child(6) td+ td::text').extract()> 0:
                phone = response.css('tr:nth-child(6) td+ td::text').extract()[0].encode('utf8')
            else:
                phone = response.css('tr:nth-child(6) td+ td::text').extract().encode('utf8')

            if response.css('tr:nth-child(2) td+ td::text').extract()> 0:
                pitch_addr = response.css('tr:nth-child(2) td+ td::text').extract()[0].encode('utf8')
            else:
                pitch_addr = response.css('tr:nth-child(2) td+ td::text').extract().encode('utf8')

            yield {
            'pitch_name': pitch_name,
            'number': phone,
            'address': pitch_addr,
            'district': response.meta['district']
            }

# run scrapy runspider football_seven_playground_spider.py -o ../data/football-seven-playgrounds.json