import re

import scrapy
class CardLinksSpider(scrapy.Spider):
    
    name = "card_links"
    # allowed_domains = ["digimoncardgame.fandom.com"]
    # start_urls = ["https://digimoncardgame.fandom.com/wiki/Booster_Packs"]
    
    custom_settings = {
        "ITEM_PIPELINES" : {
            "scraper.pipelines.CardLinksPipeline": 1,
        },
    }

    def __init__(self, url=None, set_name = None, set_id= None, *args, **kwargs):
        super(CardLinksSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://digimoncardgame.fandom.com{url}"]
        self.set_name = set_name
        self.set_id = set_id

    # async def start (self):
    #     self.log ("Start called")
    #     self.log ("Scraping page {}".format( self.url))

    #     # yield scrapy.Request (f"digimoncardgame.fandom.com{self.url}", self.parse)

    def parse (self, response):

        for link in response.css(".cardlist")[0].xpath(".//tbody//tr/th/a"):
            url = link.xpath("@href").extract_first().strip()
            card_name = link.xpath ("text()").extract_first().strip()
            card_id = re.findall (r"[A-Z]+\d+-\d*", card_name)[-1]
            # self.log ("{} card id".format(card_id))
            self.log ("Found card {} at {}".format(card_name, url))

            yield {
                "card_id" : card_id,
                "card_name": card_name,
                "link" : url,
                "set_name": self.set_name,
                "set_id": self.set_id
            }
