import scrapy
import pandas as pd

class QuotesSpider(scrapy.Spider):
    name = "reviews"

    """
    start_urls = [
        "https://www.trustpilot.com/review/baileyscbd.com",
    ]
    """

    df = pd.read_json('C:/Users/kting/Documents/GitHub/post-tuto-deployment/src/scraping/myscrapy/trustpilot/trustpilot/spiders/subcategories.jl', lines=True)
    start_urls = list(df['company_uri'])[:]

    def parse(self, response):
        
        company_name = response.xpath("//span[@class='multi-size-header__big']/text()").get()
        company_website = response.xpath("//a[@class='badge-card__section badge-card__section--hoverable company_website']/@title").get()
        company_logo = response.xpath("//img[@class='business-unit-profile-summary__image']/@src").get()
        
        # each page contains up to 20 cards, each card contains 1 comment and 1 rating
        for card in response.xpath("//div[@class='review-list']/div[contains(@class, 'review-card')]"):
        
            # COMMENT =================
            comment_body = card.xpath(".//div[@class='review-content__body']") # comment body
            comment      = comment_body.xpath("./p/text()").get() # Attempt to extract "Comment Desc." Most, but not all reviews have these.
            if comment is None:
                comment = comment_body.xpath("./h2/a/text()").get() # We use "Comment Title", which ALL reviews have.
            else:
                comment = comment.strip() # We use "Comment Desc."
            
            # RATING ==================
            rating = card.xpath(".//div[contains(@class, 'star-rating')]/img/@alt").get()[0]
                
            # YIELD ===================
            yield {
                'company_name': company_name,
                'company_website': company_website,
                'company_logo': company_logo,
                'review_url': response.url,
                'comment': comment,
                'rating': rating,
            }
    
        next_page = response.xpath("//a[@data-page-number='next-page']")
        if next_page.xpath("./text()").get() is not None:
            yield response.follow(next_page[0], callback=self.parse)
            

        """
        next_page = response.xpath("//a[contains(@class, 'paginationLinkNext')]")
        if len(next_page) == 1:
            yield response.follow(next_page[0], callback=self.parse)
        """
