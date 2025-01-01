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

            yield response.follow(url, self.parse_card)

    def parse_card (self, response):

        name_eng = response.xpath(".//tr/td[text() = 'Name']/following-sibling::td/*/text()").get()
        name_jpn = response.xpath(".//tr/td[text() = 'Japanese']/following-sibling::td/text()").get().replace('\n', '')
        name_tchn = response.xpath(".//tr/td[text() = 'Traditional Chinese']/following-sibling::td/text()").get().replace('\n', '')
        name_schn = response.xpath(".//tr/td[text() = 'Simplified Chinese']/following-sibling::td/text()").get().replace('\n', '')
        name_kor = response.xpath(".//tr/td[text() = 'Korean']/following-sibling::td/text()").get().replace('\n', '')
        colour = response.xpath(".//tr/td[text() = 'Colour']/following-sibling::td/*/text()").getall()

        card_type = response.xpath(".//tr/td[text() = 'Card Type']/following-sibling::td/*/text()").get()

        level = response.xpath(".//tr/td[text() = 'Level']/following-sibling::td/*/text()").get()
        form = response.xpath(".//tr/td[text() = 'Form']/following-sibling::td/*/text()").get()
        type = response.xpath(".//tr/td[text() = 'Type']/following-sibling::td/*/text()").getall()
        rarity  = response.xpath(".//tr/td[text() = 'Rarity']/following-sibling::td/*/text()").get()
        evo_conditions = list()

        evo_con_elements = response.css (".evocon")
        for condition in evo_con_elements:
            evo_conditions.append (condition.xpath(".//*//text()").getall())


        card_effects = response.css(".effect tr")[1].xpath("./td//text()").getall()  


        restrictions = response.css (".restricted > tr").xpath("./td//*//text()")
        # evo_con_elements = [i for i in evo_con_elements if '\n' not in i]

        # for evo_con in evo_con_elements:
        #     evo_colour = evo_con.css ("tbody > tr > td")

        #     evo_conditions.append({"colour": })


        self.log ("Parsing card {} with id {}".format(name_eng, 0 ))

        yield {
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
        }
        

        

             
