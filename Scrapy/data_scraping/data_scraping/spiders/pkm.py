# -*- coding: utf-8 -*-
from typing import Any, Callable

import scrapy


class PkmSpider(scrapy.Spider):
    name = 'pkm'
    allowed_domains = ['pokemondb.net']
    start_urls = ['http://pokemondb.net/pokedex/bulbasaur']

    def parse(self, response):
        name = response.xpath('//h1/text()').extract_first()
        number = response.xpath('//*[@class="vitals-table"]//tbody/tr/td/strong/text()').extract_first()

        pktype = response.xpath('//*[@class="vitals-table"]/tbody/tr/td')[1].xpath('a/text()').extract()
        pkspecies = response.xpath('//*[@class="vitals-table"]/tbody/tr/td')[2].xpath('text()').extract()
        pkheight = response.xpath('//*[@class="vitals-table"]/tbody/tr/td')[3].xpath('text()').extract()
        pkweight = response.xpath('//*[@class="vitals-table"]/tbody/tr/td')[4].xpath('text()').extract()
        pkabilities = response.xpath('//*[@class="vitals-table"]/tbody/tr/td')[4] \
            .xpath('//*[@class="text-muted"]/a/text()').extract()

        # Base stats
        pkhp = response.xpath('//*[@class="vitals-table"]')[1].xpath('//*[@class="cell-num"]')[0] \
            .xpath('text()').extract()
        pkattack = response.xpath('//*[@class="vitals-table"]')[1].xpath('//*[@class="cell-num"]')[3] \
            .xpath('text()').extract()
        pkdefense = response.xpath('//*[@class="vitals-table"]')[1].xpath('//*[@class="cell-num"]')[6] \
            .xpath('text()').extract()
        pkspatk = response.xpath('//*[@class="vitals-table"]')[1].xpath('//*[@class="cell-num"]')[9] \
            .xpath('text()').extract()
        pkspdef = response.xpath('//*[@class="vitals-table"]')[1].xpath('//*[@class="cell-num"]')[12] \
            .xpath('text()').extract()
        pkspeed = response.xpath('//*[@class="vitals-table"]')[1].xpath('//*[@class="cell-num"]')[15] \
            .xpath('text()').extract()

        dict_stats = {"hp": pkhp,
                      "Attack": pkattack,
                      "pkdefense": pkdefense,
                      "SpAtk": pkspatk,
                      "pkspdef": pkspdef,
                      "Speed": pkspeed, }

        # Type defenses
        nor = response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[0].xpath('text()').extract()
        fir = response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[1].xpath('text()').extract()
        wat = response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[2].xpath('text()').extract()
        ele = response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[3].xpath('text()').extract()
        gra = response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[4].xpath('text()').extract()
        ice = response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[5].xpath('text()').extract()
        fig = response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[6].xpath('text()').extract()
        poi = response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[7].xpath('text()').extract()
        gro = response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[8].xpath('text()').extract()
        fly = response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[9].xpath('text()').extract()
        psy = response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[10].xpath('text()').extract()
        bug = response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[11].xpath('text()').extract()
        roc = response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[12].xpath('text()').extract()
        gho = response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[13].xpath('text()').extract()
        dra = response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[14].xpath('text()').extract()
        dar = response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[15].xpath('text()').extract()
        ste = response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[16].xpath('text()').extract()
        fai = response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[17].xpath('text()').extract()

        dict_defenses = {"nor": nor,
                         "fir": fir,
                         "wat": wat,
                         "ele": ele,
                         "gra": gra,
                         "ice": ice,
                         "fig": fig,
                         "poi": poi,
                         "gro": gro,
                         "fly": fly,
                         "psy": psy,
                         "bug": bug,
                         "roc": roc,
                         "gho": gho,
                         "dra": dra,
                         "dar": dar,
                         "ste": ste,
                         "fai": fai}

        # recuperar propriedade title
        # response.xpath('//*[@class="type-table type-table-pokedex"]/tr/td')[0].xpath('@title').extract()

        yield {
            "name": name,
            "number": number,
            "type": pktype,
            "species": pkspecies,
            "height": pkheight,
            "weight": pkweight,
            "abilities": pkabilities,
            "stats": dict_stats,
            "defenses": dict_defenses

        }

        next_page_url = response.xpath('//*[@class="entity-nav-next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(absolute_next_page_url)
