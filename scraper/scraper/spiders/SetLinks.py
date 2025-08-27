import scrapy


class SetLinksSpider(scrapy.Spider):
    
    name = "set_links"
    # allowed_domains = ["digimoncardgame.fandom.com"]
    start_urls = ["https://digimoncardgame.fandom.com/wiki/Booster_Packs"]

    def parse(self, response):
        for link in response.xpath("//tr[@class=\"{{{bodyclass}}}\"]//a"):
            set_name = link.css ("a::text").extract_first().strip()
            url = link.xpath("@href").extract_first().strip()
            # self.log ("Found set {} at {}".format(set_name, url))
            yield {
                "set_name": set_name,
                "link": url,
            }


    
    
        

        

             

        
        