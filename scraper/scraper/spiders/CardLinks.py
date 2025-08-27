import scrapy
class CardLinksSpider(scrapy.Spider):
    
    name = "card_links"
    # allowed_domains = ["digimoncardgame.fandom.com"]
    # start_urls = ["https://digimoncardgame.fandom.com/wiki/Booster_Packs"]
    
    def __init__(self, url=None, *args, **kwargs):
        super(CardLinksSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://digimoncardgame.fandom.com{url}"]

    # async def start (self):
    #     self.log ("Start called")
    #     self.log ("Scraping page {}".format( self.url))

    #     # yield scrapy.Request (f"digimoncardgame.fandom.com{self.url}", self.parse)

    def parse (self, response):

        for link in response.css(".cardlist")[0].xpath(".//tbody//tr/th/a"):
            url = link.xpath("@href").extract_first().strip()
            card_name = link.xpath ("text()").extract_first().strip()

            self.log ("Found card {} at {}".format(card_name, url))

            yield {
                "card_name": card_name,
                "link" : url,
            }
