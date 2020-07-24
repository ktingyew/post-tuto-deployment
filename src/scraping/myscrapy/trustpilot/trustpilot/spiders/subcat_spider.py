import scrapy
import pandas as pd

class QuotesSpider(scrapy.Spider):
    name = "subcategory"

    df = pd.read_csv('C:/Users/kting/Documents/GitHub/post-tuto-deployment/src/scraping/myscrapy/trustpilot/trustpilot/spiders/subcaturls.csv')
    start_urls = list(df['URL'])[:]

    def parse(self, response):
        
        category = response.xpath("//a[@target='_self']/span[2]/text()").get()
        subcategory = response.xpath("//h1[contains(@class, 'categoryBusinessHeaderTitle')]/text()").get()[8:]
            
        for c in response.xpath("//div[contains(@class, 'businessUnitCardsContainer')][1]/a"):
            yield {
                'category': category,
                'subcategory': subcategory,
                'company_name': c.xpath("./div/div/div/div[contains(@class, 'businessTitle')]/text()").get(),
                'company_uri': "https://www.trustpilot.com" + c.xpath("./@href").get(),
            }

        next_page = response.xpath("//a[contains(@class, 'paginationLinkNext')]")
        if len(next_page) == 1:
            yield response.follow(next_page[0], callback=self.parse)
            
