import scrapy


class Spider(scrapy.Spider):
    name = 'teams'
    # start_urls = ['http://www.591.com.hk/home/index/deal?t=default&p='+str(i) for i in range(1,547)]
    start_urls = ['http://www.times-footballclub.com/com_team.php?match_name=90']

    def parse(self, response):
        for table in response.css('td td td td table table'):
            if len(table.css('strong'))>0:

                yield {
                    'teamname': table.css('strong::text')[0].extract().encode('utf-8'),
                    'image-url': response.urljoin(table.css('a img::attr(src)')[0].extract()),
                    'form-year': table.css('tr:nth-child(2) tr:nth-child(2) td:nth-child(2)::text')[0].extract(),
                    'active-area': table.css('tr:nth-child(2) tr:nth-child(3) td:nth-child(2)::text')[0].extract().encode('utf8'),
                    'average-age': table.css('tr:nth-child(2) tr:nth-child(4) td:nth-child(2)::text')[0].extract()
                }


# run scrapy runspider football_seven_teams.py -o ../data/teams.json