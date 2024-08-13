import scrapy


class CardsSpider(scrapy.Spider):
    name = "cards"
    allowed_domains = ["digimoncardgame.fandom.com"]
    start_urls = ["https://digimoncardgame.fandom.com/wiki/Booster_Packs"]

    def parse(self, response):
        for link in response.xpath("//tr[@class=\"{{{bodyclass}}}\"]//a").getall():
            set_name = link.css ("a::text").extract_first().strip()
            url = start_urls[0] + link.xpath("@href").extract_first().strip()
            self.log ("Found set {} at {}".format(set_name, url))
            yield ""
