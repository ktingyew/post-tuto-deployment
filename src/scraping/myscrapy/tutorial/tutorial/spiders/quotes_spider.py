import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]


    def parse(self, response):
        for q in response.xpath("//div[@class='quote']"):
            yield {
                'quote': q.xpath("./span[@class='text']/text()").get(),
                'author': q.xpath("./span/small/text()").get(),
                'tags': q.xpath("./div/meta/@content").get(),
            }
 
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page is not None:
            yield scrapy.follow(next_page, callback=self.parse)