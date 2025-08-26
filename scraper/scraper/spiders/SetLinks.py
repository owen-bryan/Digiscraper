import scrapy


class SetLinksSpider(scrapy.Spider):
    
    name = "set_links"
    # allowed_domains = ["digimoncardgame.fandom.com"]
    start_urls = ["https://digimoncardgame.fandom.com/wiki/Booster_Packs"]

    def parse(self, response):
        for link in response.xpath("//tr[@class=\"{{{bodyclass}}}\"]//a"):
            # print(link)
            set_name = link.css ("a::text").extract_first().strip()
            url = link.xpath("@href").extract_first().strip()
            # self.log ("Found set {} at {}".format(set_name, url))
            yield {
                "set_name": set_name,
                "link": url,
            }

            # yield response.follow (url, self.parse_set)



    

    def parse_art_urls (self, response):
        def extract_img_url  (raw_img_url):
            result = list()
            for url in raw_img_url:
                if url.find("data:image") == -1:
                    result.append(url.split("/revision/")[0])

            return result

        result = dict()

        eng_art_url = extract_img_url(response.xpath("//div[@id='gallery-0']//img/@src").getall())
        # jpn_art_url = extract_img_url(response.xpath("//div[@id='gallery-1']//img/@src").getall())
        # chn_art_url = extract_img_url(response.xpath("//div[@id='gallery-2']//img/@src").getall())
        # kor_art_url = extract_img_url(response.xpath("//div[@id='gallery-3']//img/@src").getall())


        # eng_art_url = extract_img_url(response.xpath("//div[@id='gallery-0']//a[@class='image lightbox']/@href").getall())
        # jpn_art_url = extract_img_url(response.xpath("//div[@id='gallery-1']//a[@class='image lightbox']/@href").getall())
        # chn_art_url = extract_img_url(response.xpath("//div[@id='gallery-2']//a[@class='image lightbox']/@href").getall())
        # kor_art_url = extract_img_url(response.xpath("//div[@id='gallery-3']//a[@class='image lightbox']/@href").getall())



        if eng_art_url is not None:
            # result ["eng"] = list(zip (eng_art_url, eng_art_key))
            yield {"image_urls": eng_art_url}
            
            # for image_url in eng_art_url:
            #     yield {"file_urls": [image_url]}
        # if jpn_art_url is not None:
        #     result ["jpn"] = list(zip (jpn_art_url, jpn_art_key))
        #     yield {"file_urls": jpn_art_url}
        #     # for image_url in jpn_art_url:
        #     #     yield {"file_urls": [image_url]}
        # if chn_art_url is not None:
        #     result ["chn"] = list(zip (chn_art_url, chn_art_key))
        #     yield {"file_urls": chn_art_url}
        #     # for image_url in chn_art_url:
        #     #     yield {"file_urls": [image_url]}
        # if kor_art_url is not None:
        #     result ["kor"] = list(zip (kor_art_url, kor_art_key))
        #     yield {"file_urls": kor_art_url}
        #     # for image_url in jpn_art_url:
        #     #     yield {"file_urls": [image_url]}

        # yield result

    
    
        

        

             

        
        