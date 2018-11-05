# -*- coding: utf-8 -*-
import logging
from urllib.request import urlopen, urljoin

from lxml import etree

logger = logging.getLogger(__name__)


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
        info = {}
        info['name'] = each.xpath('./td[position()=1]/a/text()')[0].strip()
        info['id'] = int(each.xpath('./@data-campaign-id')[0].strip())
        info['image'] = each.xpath('.//img/@data-src')[0]

        try:
            info['description'] = each.xpath('.//p/text()')[0].strip()
        except Exception as err:
            logger.warning(err)

        try:
            info['url'] = each.xpath('.//a/@href')[0].strip()
        except Exception as err:
            logger.warning(err)
        else:
            if info['url'].startswith('#'):
                info['url'] = urljoin(subcategory_url, info['url'])

        try:
            info['reviews'] = int(
                each.xpath('.//a/text()')[1].strip().split()[1])
        except Exception as err:
            logger.warning(err)
            info['reviews'] = 0

        try:
            info['rating'] = float(
                each.xpath('.//div[@data-rating]/@data-rating')[0])
        except Exception as err:
            logger.warning(err)

        companies.append(info)

    return sorted(
        companies, key=lambda x: int(x.get('reviews', 0)), reverse=True)
