# -*- coding: utf-8 -*-
import logging

from ..utils.parser import Parser
from .base_spider import BaseSpider

logger = logging.getLogger(__name__)


class CompaniesSpider(BaseSpider):
    """Crawl the companies for a particular category"""
    name = 'companies_crawler'
    allowed_domains = ['consumeraffairs.com']
    start_urls = ['https://www.consumeraffairs.com/']

    def parse(self, response):
        # Page related parse
        parser = Parser(response)
        parser.add_xpath_rule(
            'breadcrumbs',
            '//div[@class="breadcrumbs"]//li[position()>1]//text()',
            as_list=True)
        page_data = parser.parse()

        # for company in response.css('tr.category-listing-campaign'):
        for company in response.xpath('//tr[@data-campaign-id]'):
            logger.debug('Parsing company %s', company)

            # Company related parse
            parser = Parser(company)

            parser.add_css_rule(
                'campaign_id',
                '::attr(data-campaign-id)')

            parser.add_xpath_rule(
                'company_name',
                # '.category-listing-campaign__title > div > a::text')
                './td[position()=1]/a/text()')

            parser.add_xpath_rule(
                'company_description',
                './td/p/text()')
                # '.category-listing-campaign__description > p::text')

            # parser.add_css_rule(
            #     'company_link',
            #     '.category-listing-campaign__title > div > a::attr(href)')

            parser.add_xpath_rule(
                'short_url',
                './td[position()=1]/a/@href',
                # '.category-listing-campaign__title > div > a::attr(href)',
                regex=r'(?:\.com/)(.*?)/?$')

            # parser.add_css_rule(
            #     'rating',
            #     '.category-listing-campaign__review > div::attr(data-rating)')

            # parser.add_css_rule(
            #     'reviews_count',
            #     '.category-listing-campaign__review > a::text',
            #     regex=r'(\d+)')

            parser.add_css_rule(
                'image_url',
                'img::attr(data-src)')

            parsed = parser.parse()
            parsed.update(page_data)
            yield parsed
