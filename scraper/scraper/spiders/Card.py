import scrapy

class CardSpider (scrapy.Spider):
    name = "card"
    def __init__(self, url=None, set_id = None, set_name = None, card_id = None, *args, **kwargs):
        super(CardSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://digimoncardgame.fandom.com{url}"]
        self.set_name = set_name
        self.set_id = set_id
        self.card_id = card_id


    def remove_newline_character (self, item):
        if item is not None:
            return item.replace ('\n', '').strip()
        return item
    

    def parse (self, response):
        card_id = response.css(".cardno::text").get().replace('(', '').replace(')', '')
        name_eng = response.xpath(".//tr/td[text() = 'Name']/following-sibling::td/*/text()").get()

        # name_jpn = self.remove_newline_character(response.xpath(".//tr/td[text() = 'Japanese']/following-sibling::td/text()").get())
        # name_tchn = self.remove_newline_character(response.xpath(".//tr/td[text() = 'Traditional Chinese']/following-sibling::td/text()").get())
        # name_schn = self.remove_newline_character(response.xpath(".//tr/td[text() = 'Simplified Chinese']/following-sibling::td/text()").get())
        # name_kor = self.remove_newline_character(response.xpath(".//tr/td[text() = 'Korean']/following-sibling::td/text()").get())
        # colour = response.xpath(".//div[@class='info-main']//td[text() = 'Colour']/following-sibling::td//a//text()").getall()

        # card_type = response.xpath(".//tr/td[text() = 'Card Type']/following-sibling::td/*/text()").get()

        # level = response.xpath(".//tr/td[text() = 'Level']/following-sibling::td/*/text()").get()
        # form = response.xpath(".//tr/td[text() = 'Form']/following-sibling::td/*/text()").get()
        # type = response.xpath(".//tr/td[text() = 'Type']/following-sibling::td/*/text()").getall()
        # rarity  = response.xpath(".//tr/td[text() = 'Rarity']/following-sibling::td/*/text()").get()
        # evo_conditions = list()

        # evo_con_elements = response.css (".evocon")
        # for condition in evo_con_elements:
        #     evo_conditions.append (condition.xpath(".//*//text()").getall())


        # card_effects = response.css(".info-extra > .effect").xpath(".//td//text()").getall()  
        # inherited_effects = None

        # # self.log (card_effects)

        # if card_effects is not None:
        #     if (len(card_effects) >= 2):
        #         card_effects = ' '.join(card_effects[0]).strip()
        #         inherited_effects = ' '.join(card_effects[1]).strip()
        #     else:
        #         card_effects = ' '.join(card_effects).strip()

        # restrictions = dict()

        # restrictions["eng"] = response.xpath("//th[contains(text(), 'English')]/following-sibling::td/a/text()").get()
        # restrictions["jpn"] = response.xpath("//th[contains(text(), 'Japanese')]/following-sibling::td/a/text()").get()
        # restrictions["chn"] = response.xpath("//th[contains(text(), 'Chinese')]/following-sibling::td/a/text()").get()
        # restrictions["kor"] = response.xpath("//th[contains(text(), 'Korean')]/following-sibling::td/a/text()").get()


        # self.log ("Parsing card {} with id {}".format(name_eng, card_id ))

        yield {
            "card_id": card_id,
            "name_eng": name_eng,
            "set_id": self.set_id,
            "set_name": self.set_name,
            # "name_jpn": name_jpn,
            # "name_tchn": name_tchn,
            # "name_schn": name_schn,
            # "name_kor": name_kor,
            # "colour": colour,
            # "card_type": card_type,
            # "level": level,
            # "form": form,
            # "type": type,
            # "rarity": rarity,
            # "evo_conditions": evo_conditions,
            # "restrictions": restrictions,
            # "card_effect" : card_effects,
            # "inherited_effect": inherited_effects,
        }
