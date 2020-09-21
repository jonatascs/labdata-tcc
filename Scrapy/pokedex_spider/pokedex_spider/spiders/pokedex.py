# -*- coding: utf-8 -*-
import scrapy


class PokedexSpider(scrapy.Spider):
    name = 'pokedex'
    allowed_domains = ['pokemon.com']
    start_urls = ['http://www.pokemon.com/br/pokedex/bulbasaur']

    def parse(self, response):

        ##teste

        # response.xpath('//*[@class="section pokedex-pokemon-details"].//*[@class="pokemon-stats-info active"]')

        ###teste

        pokemon_name = response.xpath('//*[@class="pokedex-pokemon-pagination-title"]/div/text()').extract_first()

        # print("Nome: "+pokemon_name.strip())
        # pokemon_number = response.xpath('//*[@class="pokemon-number"]/text()').extract_first()

        pokemon_number = response.xpath('//*[@class="pokedex-pokemon-pagination-title"]/div/span/text()').extract_first()
        # print("Numero: "+pokemon_number.strip())
        pokemon_img_link = response.xpath('//*[@class="profile-images"]//img/@src').extract_first()
        # print("img: "+pokemon_img_link.strip())
        pokemon_about = response.xpath('//*[@class="version-descriptions active"]/p/text()').extract_first()
        # print("Sobre: "+pokemon_about.strip())

        ##impar label / par descrição
        listPropt = response.xpath('//*[@class="pokemon-ability-info color-bg color-lightblue match active"]//li')

        dict_hab = {}

        ##está errado as habilidades pode ter mais de uma... e o retorna  não precisa fazer um for, apenas pegar nas variaveis
        for prop in listPropt:
            dict_hab[prop.xpath('.//*[@class="attribute-title"]/text()').extract_first()] = prop.xpath(
                './/*[@class="attribute-value"]/text()').extract_first()

        # print(dict_hab)
        ##retona descrição da habilidade do pokemon
        pokemon_info_abilities_detail = response.xpath(
            '//*[@class="pokemon-ability-info-detail match"]//p/text()').extract_first()
        # print("Descrição das habilidades: "+pokemon_info_abilities_detail.strip())

        ##retorna lista do Tipo do pokemon
        pokemon_list_type_temp = response.xpath('//*[@class="dtm-type"]//li//a/text()').extract()
        pokemon_list_type = []
        for p in pokemon_list_type_temp:
            pokemon_list_type.append(p.strip())

        # retorna lista fraquezas do pokemon
        pokemon_list_weaknesses_temp = response.xpath('//*[@class="dtm-weaknesses"]//li//a//span/text()').extract()
        pokemon_list_weaknesses = []
        # print("Fraquesas: "+pokemon_list_weaknesses)
        for p in pokemon_list_weaknesses_temp:
            pokemon_list_weaknesses.append(p.strip())
        #retornar a estatistica do pokemon
        pokemon_stats = response.xpath(
            '//*[@class="pokemon-stats-info active"]/ul/li//*[@class="gauge"]//*[@class="meter"]/@data-value').extract()


        yield {
            "name": pokemon_name.strip(),
            "number": pokemon_number.replace('Nº', '').strip(),
            "img": pokemon_img_link.strip(),
            "about": pokemon_about.strip(),
            "info": dict_hab,
            "detail_abilities": pokemon_info_abilities_detail.strip(),
            "type": pokemon_list_type,
            "weaknesses": pokemon_list_weaknesses,
            'hp': pokemon_stats[0],
            'attack': pokemon_stats[1],
            'defense': pokemon_stats[2],
            'special_attack': pokemon_stats[3],
            'special_defense': pokemon_stats[4],
            'speed': pokemon_stats[5]
        }

        # next page
        # pagina = response.xpath('//*[@class="pokedex-pokemon-pagination"]/a/@href')[1].extract()
        # print("Proxima Pagina: "+pagina.strip())

        next_page_url = response.xpath('//*[@class="pokedex-pokemon-pagination"]/a/@href')[1].extract()

        absolute_next_page_url = response.urljoin(next_page_url)

        yield scrapy.Request(absolute_next_page_url)
        # yield
