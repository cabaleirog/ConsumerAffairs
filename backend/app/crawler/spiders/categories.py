# -*- coding: utf-8 -*-
import logging
from urllib.request import urlopen

from lxml import etree

CATEGORIES_URL = 'https://www.consumeraffairs.com/resources'

logger = logging.getLogger(__name__)


def fetch_categories():
    htmlparser = etree.HTMLParser()
    response = urlopen(CATEGORIES_URL)
    tree = etree.parse(response, htmlparser)

    categories = []
    for card in tree.xpath('//div/a[@href="#"]'):
        category = dict(
            name=card.xpath('./div[last()]//strong/text()')[0],
            description=card.xpath('./div[last()]//span/text()')[0],
            url=card.xpath('.//following-sibling::div/div[last()]/a/@href')[0],
            subcategories=[])
        for subcategory in card.xpath('.//following-sibling::div/div/a')[:-1]:
            sub = dict(
                name=subcategory.xpath('./span/text()')[0],
                url=subcategory.xpath('./@href')[0])
            category['subcategories'].append(sub)
        categories.append(category)

    return categories


def fetch_sub_categories(category_url):
    """---

    Args:
        category_url (str):
            ie. https://www.consumeraffairs.com/moving-checklist

    """
    htmlparser = etree.HTMLParser()
    response = urlopen(category_url)
    tree = etree.parse(response, htmlparser)

    sub_categories = []
    for topic in tree.xpath('//h2'):
        for link in topic.xpath('./following-sibling::ul//a'):
            sub_category = dict(
                name=link.xpath('./text()')[0],
                topic=topic.xpath('./text()')[0],
                # description=topic.xpath('./following-sibling::p/text()')[0],
                description='',
                url=link.xpath('./@href')[0])
            sub_categories.append(sub_category)

    return sub_categories


def fetch_companies(subcategory_url):
    """---

    Args:
        subcategory_url (str):
            ie. https://www.consumeraffairs.com/education/online-colleges

    """
    htmlparser = etree.HTMLParser()
    response = urlopen(subcategory_url)
    tree = etree.parse(response, htmlparser)

    companies = []
    for each in tree.xpath('//tr[@data-campaign-id]'):
        companies.append(dict(
            name=each.xpath('./td[position()=1]/a/text()')[0],
            # description=,
            # campaign_id=,
            # image_url=,
        ))
        # for link in topic.xpath('./following-sibling::ul//a'):
        #     sub_category = dict(
        #         name=link.xpath('./text()')[0],
        #         topic=topic.xpath('./text()')[0],
        #         # description=topic.xpath('./following-sibling::p/text()')[0],
        #         description='',
        #         url=link.xpath('./@href')[0])
        #     companies.append(sub_category)

    return companies

"""
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
"""
