# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime


class CruisesSpider(scrapy.Spider):
    name = 'cruises'
    allowed_domains = ['www.lueftner-cruises.com']
    start_urls = ['http://www.lueftner-cruises.com/en/river-cruises/cruise.html']
    base_url = 'http://www.lueftner-cruises.com/'

    results = []

    def parse(self, response):
        ''' Parsing links from start_urls list '''
        all_urls = response.css('.travel-box-container .yearContainer a::attr(href)').extract()
        urls = []
        # Push items if not present in urls
        [urls.append(item) for item in all_urls if item not in urls]
        # Start parse first 4 urls
        for url in urls[:4]:
            yield scrapy.Request(self.base_url+url, callback = self.parse_links)

    def parse_links(self, response):
        ''' Parsing links from parse method '''
        dates = {}
        # iterating through available dates and ships.
        for sel in response.css('.accordeon-panel-default'):
            try:
                date = sel.css('.price-duration::text').get().split('-')[0].strip()
                date_conv = datetime.strptime(date, '%d. %b %Y').strftime('%Y-%m-%d')
                dates[date_conv] = {
                    'ship': sel.css('.table-ship-name::text').get(),
                    'price' : float(sel.css('.price-ship .pull-right .big-table-font::text').get().strip()[2:].
                                    replace('.','').replace(',','.'))
                }
            except ValueError:
                print('Cannot convert date')
                continue

        name = response.css('.cruise-headline h1::text').get() or 'N/A'
        days = response.css('.cruise-duration::text').get().strip().split()[0]
        days = int(days) if days.isdigit() else 'N/A'
        itinerary = [item.strip().split('>')[0] for item in response.css('.route-city::text').extract()]

        # Yielding back a parsing result
        yield {
            'name': name,
            'days': days,
            'itinerary': itinerary,
            'dates': dates,
        }

