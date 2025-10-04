import scrapy

class CardArtSpider (scrapy.Spider):

    name = "card_art"
    custom_settings = {
        "ITEM_PIPELINES" : {
            "scraper.pipelines.CardArtPipeline": 1,
        },
        "IMAGES_STORE": "images",
    }

    def __init__(self, url=None, card_id = None, set_number = None, *args, **kwargs):
        super(CardArtSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://digimoncardgame.fandom.com{url}/Gallery"]
        self.card_id = card_id
        self.set_number = set_number


    def parse (self, response):
        def extract_img_url  (raw_img_url):
            result = list()
            for url in raw_img_url:
                if url.find("data:image") == -1:
                    result.append(url.split("/revision/")[0])

            return result

        # result = dict()

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
            yield {"image_urls": eng_art_url, "id": self.card_id}

            
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
