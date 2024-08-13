import scrapy


class CardsSpider(scrapy.Spider):
    name = "cards"
    allowed_domains = ["digimoncardgame.fandom.com"]
    start_urls = ["https://digimoncardgame.fandom.com/wiki/Booster_Packs"]

    def parse(self, response):
        for link in response.xpath("//tr[@class=\"{{{bodyclass}}}\"]//a"):
            # print(link)
            set_name = link.css ("a::text").extract_first().strip()
            url = link.xpath("@href").extract_first().strip()
            self.log ("Found set {} at {}".format(set_name, url))
            yield {
                "set_name": set_name,
                "link": url,
            }

            yield response.follow (url, self.parse_set)

    def parse_set (self, response):

        for link in response.css(".cardlist")[0].xpath(".//tbody//tr/th/a"):
            url = link.xpath("@href").extract_first().strip()
            card_name = link.xpath ("text()").extract_first().strip()

            self.log ("Found card {} at {}".format(card_name, url))

            yield {
                "card_name": card_name,
                "link" : url,
            }

