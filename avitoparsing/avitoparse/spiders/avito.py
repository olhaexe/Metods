# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/kvartiry/prodam']

    def parse(self, response: HtmlResponse):
        pages = response.css('div.pagination-hidden-3jtv4 div.pagination-pages a.pagination-page::attr(href)').extract()
        # div.index-content-2lnSO div.js-pages pagination-pagination-2j5na div.pagination-hidden-3jtv4 div.pagination-pages a.pagination-page::attr(href)
        for page in pages:
            yield response.follow(page, callback=self.parse)
        adverts = response.css('div.description div.item_table-header div.snippet-title-row h3.snippet-title a.snippet-link::attr(href)').extract()
        # div.item-line div.item-table-wrapper div.description div.item_table-header div.snippet-title-row h3.snippet-title a.snippet-link::attr(href)
        for advert in adverts:
            yield response.follow(advert, callback=self.advert_parse)

    def advert_parse(self, response: HtmlResponse):
        title = response.css('span.title-info-title-text::text').extract_first()
        price = response.css('span.js-item-price::attr(content)').extract_first()
        parameters = response.css('li.item-params-list-item').extract()
        for i in range(len(parameters)):
            parameters[i] = parameters[i].replace('<li class="item-params-list-item"> ', '')
            parameters[i] = parameters[i].replace('<span class="item-params-label">', '')
            parameters[i] = parameters[i].replace('</span>', '')
            parameters[i] = parameters[i].replace('</li>', '')

        yield {'title': title, 'price': price, 'parameters': parameters}
