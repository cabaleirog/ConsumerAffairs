# # -*- coding: utf-8 -*-
# import re
# import logging

# from scrapy.http import Request
# from scrapy.crawler import Crawler
# from scrapy.settings import Settings

# from ..utils.parser import Parser
# from .base_spider import BaseSpider
# from .categories import CategoriesSpider
# from .companies import CompaniesSpider
# from .reviews import ReviewsSpider

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


# class FullSiteSpider(BaseSpider):
#     """Crawl the reviews for a particular company"""
#     name = 'all_reviews_crawler'
#     allowed_domains = ['consumeraffairs.com']
#     start_urls = ['https://www.consumeraffairs.com/resources/']
#     handle_httpstatus_list = [302]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.download_delay = 1

#     def parse(self, response):
#         for category in response.xpath('//dd/a'):
#             url = category.xpath('.//@href').re(r'\.com\/(.*?)/?$')[0]
#             long_url = 'https://www.consumeraffairs.com/%s' % url
#             yield Request(long_url, callback=self.parse_companies)

#     def parse_companies(self, response):
#         for company in response.css('tr.category-listing-campaign'):
#             url = company.css(
#                 '.category-listing-campaign__title > div > a::attr(href)')
#             url = url.extract_first()

#             # URLs starting with '#' don't have any reviews yet
#             if url[0] == '#':
#                 continue

#             yield Request(url, callback=self.parse_reviews)

#     def parse_reviews(self, response):
#         match = re.search(
#             r'(?:\.com/)(.*?)/?(?:\?page=(\d+))?$', response.url)
#         short_url = match.group(1)
#         page = match.group(2) or 1
#         crawler = Crawler(ReviewsSpider)
#         crawler.crawl(url=short_url, page=page)
#         next_page = response.xpath(
#             "//a[contains(@class, 'js-profile-pager__next')][not(contains(@style,'display:none'))]/@href").extract_first()
#         if next_page:
#             full_url = response.urljoin(next_page)
#             yield response.follow(full_url, callback=self.parse_reviews)
