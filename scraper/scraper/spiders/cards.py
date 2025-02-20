import scrapy


class CardsSpider(scrapy.Spider):
    name = "cards"
    # allowed_domains = ["digimoncardgame.fandom.com"]
    start_urls = ["https://digimoncardgame.fandom.com/wiki/Booster_Packs"]

    def parse(self, response):
        for link in response.xpath("//tr[@class=\"{{{bodyclass}}}\"]//a"):
            # print(link)
            set_name = link.css ("a::text").extract_first().strip()
            url = link.xpath("@href").extract_first().strip()
            # self.log ("Found set {} at {}".format(set_name, url))
            # yield {
            #     "set_name": set_name,
            #     "link": url,
            # }

            yield response.follow (url, self.parse_set)

    def parse_set (self, response):

        for link in response.css(".cardlist")[0].xpath(".//tbody//tr/th/a"):
            url = link.xpath("@href").extract_first().strip()
            card_name = link.xpath ("text()").extract_first().strip()

            # self.log ("Found card {} at {}".format(card_name, url))

            # yield {
            #     "card_name": card_name,
            #     "link" : url,
            # }

            yield response.follow(url, self.parse_card)

    def parse_card (self, response):
        def remove_newline_character (item):
            if item is not None:
                return item.replace ('\n', '')

            return item


        card_id = response.css(".cardno::text").get().replace('(', '').replace(')', '')
        name_eng = response.xpath(".//tr/td[text() = 'Name']/following-sibling::td/*/text()").get()
        name_jpn = remove_newline_character(response.xpath(".//tr/td[text() = 'Japanese']/following-sibling::td/text()").get())
        name_tchn = remove_newline_character(response.xpath(".//tr/td[text() = 'Traditional Chinese']/following-sibling::td/text()").get())
        name_schn = remove_newline_character(response.xpath(".//tr/td[text() = 'Simplified Chinese']/following-sibling::td/text()").get())
        name_kor = remove_newline_character(response.xpath(".//tr/td[text() = 'Korean']/following-sibling::td/text()").get())
        colour = response.xpath(".//div[@class='info-main']//td[text() = 'Colour']/following-sibling::td//a//text()").getall()

        card_type = response.xpath(".//tr/td[text() = 'Card Type']/following-sibling::td/*/text()").get()

        level = response.xpath(".//tr/td[text() = 'Level']/following-sibling::td/*/text()").get()
        form = response.xpath(".//tr/td[text() = 'Form']/following-sibling::td/*/text()").get()
        type = response.xpath(".//tr/td[text() = 'Type']/following-sibling::td/*/text()").getall()
        rarity  = response.xpath(".//tr/td[text() = 'Rarity']/following-sibling::td/*/text()").get()
        evo_conditions = list()

        evo_con_elements = response.css (".evocon")
        for condition in evo_con_elements:
            evo_conditions.append (condition.xpath(".//*//text()").getall())


        card_effects = response.css(".info-extra > .effect").xpath(".//td//text()").getall()  
        inherited_effects = None

        self.log (card_effects)

        # if card_effects is not None:
        #     if (len(card_effects) >= 2):
        #         card_effects = ' '.join(card_effects[0]).strip()
        #         inherited_effects = ' '.join(card_effects[1]).strip()
        #     else:
        #         card_effects = ' '.join(card_effects).strip()

        restrictions = dict()

        restrictions["eng"] = response.xpath("//th[contains(text(), 'English')]/following-sibling::td/a/text()").get()
        restrictions["jpn"] = response.xpath("//th[contains(text(), 'Japanese')]/following-sibling::td/a/text()").get()
        restrictions["chn"] = response.xpath("//th[contains(text(), 'Chinese')]/following-sibling::td/a/text()").get()
        restrictions["kor"] = response.xpath("//th[contains(text(), 'Korean')]/following-sibling::td/a/text()").get()


        self.log ("Parsing card {} with id {}".format(name_eng, card_id ))

        yield {
            "card_id": card_id,
            "name_eng": name_eng,
            "name_jpn": name_jpn,
            "name_tchn": name_tchn,
            "name_schn": name_schn,
            "name_kor": name_kor,
            "colour": colour,
            "card_type": card_type,
            "level": level,
            "form": form,
            "type": type,
            "rarity": rarity,
            "evo_conditions": evo_conditions,
            "restrictions": restrictions,
            "card_effect" : card_effects,
            "inherited_effect": inherited_effects,
            # "art": card_art,
            # "errata" : response.follw ("", self.parse_errata),
            # "rulings" : response.follow ("", self.parse_rulings),
        }

        yield response.follow (response.url + "/Gallery", self.parse_art_urls)

    def parse_art_urls (self, response):
        def extract_img_url  (raw_img_url):
            result = list()
            for url in raw_img_url:
                if url.find("data:image") == -1:
                    result.append(url)

            return result

        result = dict()

        eng_art_url = extract_img_url(response.xpath("//div[@id='gallery-0']//img/@src").getall())
        jpn_art_url = extract_img_url(response.xpath("//div[@id='gallery-1']//img/@src").getall())
        chn_art_url = extract_img_url(response.xpath("//div[@id='gallery-2']//img/@src").getall())
        kor_art_url = extract_img_url(response.xpath("//div[@id='gallery-3']//img/@src").getall())


        # eng_art_url = extract_img_url(response.xpath("//div[@id='gallery-0']//a[@class='image lightbox']/@href").getall())
        # jpn_art_url = extract_img_url(response.xpath("//div[@id='gallery-1']//a[@class='image lightbox']/@href").getall())
        # chn_art_url = extract_img_url(response.xpath("//div[@id='gallery-2']//a[@class='image lightbox']/@href").getall())
        # kor_art_url = extract_img_url(response.xpath("//div[@id='gallery-3']//a[@class='image lightbox']/@href").getall())


        eng_art_key = response.xpath("//div[@id='gallery-0']//img/@data-image-key").getall()
        jpn_art_key = response.xpath("//div[@id='gallery-1']//img/@data-image-key").getall()
        chn_art_key = response.xpath("//div[@id='gallery-2']//img/@data-image-key").getall()
        kor_art_key = response.xpath("//div[@id='gallery-3']//img/@data-image-key").getall()

        if eng_art_url is not None:
            # result ["eng"] = list(zip (eng_art_url, eng_art_key))
            yield {"file_urls": eng_art_url}
            
            # for image_url in eng_art_url:
            #     yield {"file_urls": [image_url]}
        if jpn_art_url is not None:
            result ["jpn"] = list(zip (jpn_art_url, jpn_art_key))
            yield {"file_urls": jpn_art_url}
            # for image_url in jpn_art_url:
            #     yield {"file_urls": [image_url]}
        if chn_art_url is not None:
            result ["chn"] = list(zip (chn_art_url, chn_art_key))
            yield {"file_urls": chn_art_url}
            # for image_url in chn_art_url:
            #     yield {"file_urls": [image_url]}
        if kor_art_url is not None:
            result ["kor"] = list(zip (kor_art_url, kor_art_key))
            yield {"file_urls": kor_art_url}
            # for image_url in jpn_art_url:
            #     yield {"file_urls": [image_url]}

        # yield result

    
    
        

        

             

        
        