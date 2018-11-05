# -*- coding: utf-8 -*-
import logging
import re
from urllib.error import HTTPError
from urllib.request import urljoin, urlopen
from urllib.parse import urlencode

from lxml import etree

logger = logging.getLogger(__name__)


def fetch_reviews(url, page=1):
    """Crawl the reviews for a particular company.

    Args:
        company_url (str):

    """
    # company_url = urljoin('https://www.consumeraffairs.com', '/'.join(args))
    # company_url = company_url + '?' + urlencode(kwargs)

    company_url = url
    print('Parsing URL: %s' % company_url)

    # FIXME: Use urlopen. Local file is just for debug.
    # with open('fake_page.html') as file:
    #     htmlparser = etree.HTMLParser()
    #     tree = etree.parse(file, htmlparser)
    try:
        response = urlopen(company_url)
    except HTTPError:
        return [], ['HTTPError']  # FIXME: Add an useful error msg.

    if int(page) > 1 and response.url != company_url:
        # return [], []  # TODO: Return an error msg maybe?.
        return []

    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    # FIXME: --- End of debug block

    data, errors = _fetch_reviews(tree)

    # Include current page.
    data['page'] = int(page)

    return data


def _fetch_reviews(tree):
    """Crawl the reviews for a particular company.

    Args:
        tree (obj:`lxml.etree.ElementTree`):

    """
    # short_url = re.search(
    #     r'(?:\.com/)(.*?)/?(?:\?page=\d+)?$', response.url).group(1)

    # Page related parse
    # parser.add_xpath_rule(
    #     'breadcrumbs',
    #     '//div[@class="breadcrumbs"]//li[position()>1]//text()',
    #     as_list=True)
    # parser.add_css_rule(
    #     'last_updated_date', 'span.prf-rw__date::text', regex=r': (.*)')
    company_name = tree.xpath('//h1/text()')[0].strip()
    # page_data = parser.parse()

    total_reviews = int(tree.xpath('//h2/text()')[0].split()[0])
    print('Total reviews', total_reviews)

    # breadcrumbs = page_data.pop('breadcrumbs')  # We don't need to store it
    # firebase_nodes = breadcrumbs + [page_data['company'], ]

    def clean_value(value):
        return re.sub(r'[^\w\s]', '', value.strip())

    dt = tree.xpath('//h3/following-sibling::dl/dt/text()')
    dd = tree.xpath('//h3/following-sibling::dl/dd/text()')

    if len(dt) == len(dd) + 1:
        dt = dt[1:]  # Index 0 is Social media, not key/value pair.

    print(list(zip(dt, dd)))
    # print(xxxxxxxxxx)
    company_info = {'name': company_name}
    for key, value in zip(dt, dd):
        company_info[clean_value(key).replace(' ',
                                              '_').lower()] = value.strip()

    # Company logo.
    logo = tree.xpath('//div[contains(@class, "logo-box")]//img/@data-src')
    company_info['company_logo_url'] = logo[0] if logo else None

    # Review related parse
    reviews = tree.xpath('//div[@itemprop="reviews"]')
    if not reviews:
        raise Exception('Unhandled')
        # print(tree.xpath('//*'))
        # reviews = response.css('div.review')
    if not reviews:
        return None

    logger.debug(reviews)

    rv = []
    for element in reviews:
        try:
            review = parse_review(element)
        except Exception as err:
            logger.error('Unable to parse review. %s', err)
        else:
            # review['company'] = company_name
            rv.append(review)

    xxxxxx = dict(
        reviews=rv,
        total_reviews=total_reviews,
        company=company_info,
    )

    return xxxxxx, None


def parse_review(element):
    fields = [
        'stars', 'original_stars', 'original_review_date', 'review',
        'reviewer_image', 'reviewer', 'helpful', 'verified_reviewer',
        'verified_buyer', 'review_id', 'customer_response_date',
        'customer_response_text', 'company_response_date',
        'company_response_text'
    ]

    review = {field: None for field in fields}

    stars = element.xpath('.//*[@data-rating]/@data-rating')
    review['stars'] = float(stars[0]) if stars else None

    # review['rating_update'] = element.css('span.review-header-status__rating-label::text')

    text_block = element.xpath('./div[span][1]')[0]

    original_review = text_block.xpath(
        './span[contains(text(), "Original")]')[0]

    original_review_text = original_review.xpath('./text()')[0]
    match = re.match(
        r'Original review: (?P<month>\w+)\.? (?P<day>\d+), (?P<year>\d+)',
        original_review_text)
    if match:
        # TODO: Add original date as an datetime object.
        review_date = '{month} {day}, {year}'.format(**match.groupdict())
    else:
        logger.warning('Unable to match date for original review')
        review_date = None
    review['original_review_date'] = review_date
    # review['original_review_date'] = date.today().isoformat()

    paragraphs = original_review.xpath('.//following-sibling::p/text()')
    # Text inside the "Read more".
    paragraphs.extend(
        original_review.xpath('.//following-sibling::div/p/text()'))
    review['review'] = '\n'.join(x.strip() for x in paragraphs)

    author = element.xpath('.//div[div[strong[@itemprop="author"]]]')[0]

    image = author.xpath('./img/@data-src')
    review['reviewer_image'] = image[0] if image else None

    review['reviewer'] = author.xpath(
        './/strong[@itemprop="author"]/text()')[0]

    helpful = element.xpath(
        './/span[contains(@class, "helpful-count")]/strong/text()')
    review['helpful'] = int(helpful[0].split()[0]) if helpful else 0

    review['verified_reviewer'] = bool(
        author.xpath('.//strong[contains(text(), "Verified Reviewer")]'))

    # FIXME: Deprecated. Remove `is_verified` after replacing it on the UI.
    review['is_verified'] = review['verified_reviewer']

    review['verified_buyer'] = bool(
        author.xpath('.//strong[contains(text(), "Verified Buyer")]'))

    # TODO: Fix on UI and remove deprecated fields.
    review['reviewer'] = {
        'name': review['reviewer'].split(' of ')[0].strip(),
        'from': review['reviewer'].split(' of ')[1].strip(),
        'image_url': review['reviewer_image'],
        'is_verified_reviewer': review['verified_reviewer'],
        'is_verified_buyer': review['verified_buyer'],
    }

    review['review_id'] = int(element.xpath('//@data-id')[0])

    # FIXME: Deprecated. Remove `id` after replacing it on the UI.
    review['id'] = review['review_id']

    customer_response = element.xpath('.//div[@class="rvw-bd__csmr-resp"]')
    if customer_response:
        review['customer_response_date'] = customer_response[0].xpath(
            './span/text()')[0]
        review['customer_response_text'] = '\n'.join(
            [x.strip() for x in customer_response[0].xpath('./p/text()')])

        # FIXME: Dont use review['customer_response_date']
        match = re.match(
            r'Resolution response: (?P<month>\w+)\.? (?P<day>\d+), (?P<year>\d+)',
            review['customer_response_date'])
        if match:
            # TODO: Add original date as an datetime object.
            review['customer_response_date'] = '{month} {day}, {year}'.format(
                **match.groupdict())
        else:
            logger.warning('Unable to match date for original review')
            review_date = None

    else:
        # FIXME: Dont want to use an `else` here.
        review['customer_response_date'] = None
        review['customer_response_text'] = None
    #     review['customer_response_date'] = element.css('.review-body__consumer-response > span::text',
    #         regex=r'(\w+\.? \d{1,2}, \d{4})')
    #     review['customer_response_text'] = element.css('.review-body__consumer-response > p::text',
    #         as_list=True)

    company_response = element.xpath('.//div[@class="rvw-comp-resp"]')
    if company_response:
        review['company_response_date'] = company_response[0].xpath(
            './/time/@datetime')[0]
        review['company_response_text'] = '\n'.join(
            x.strip() for x in company_response[0].xpath(
                './div[contains(@class, "resp__txt")]/p/text()'))

    review['resolution_in_progress'] = bool(
        element.xpath('.//*[text()="Resolution In Progress"]'))

    #     parser.add_xpath_rule(
    #         'id',
    #         './/@data-id'
    #     )
    #     parsed['short_url'] = short_url
    # self.to_firebase('id', firebase_nodes)
    # # return self.parsed_data
    return review


# class ReviewsSpider(BaseSpider):
#     """Crawl the reviews for a particular company"""
#     name = 'reviews_crawler'
#     allowed_domains = ['consumeraffairs.com']
#     start_urls = ['https://www.consumeraffairs.com/']
#     handle_httpstatus_list = [302]

#     # @timer
#     def parse(self, response):
#         print('Parsing URL: %s' % response.url)
#         reviews = response.xpath('//div[@itemprop="reviews"]')
#         if not reviews:
#             reviews = response.css('div.review')
#         if not reviews:
#             return None

#         short_url = re.search(
#             r'(?:\.com/)(.*?)/?(?:\?page=\d+)?$', response.url).group(1)

#         # Page related parse
#         parser = Parser(response)
#         parser.add_xpath_rule(
#             'breadcrumbs',
#             '//div[@class="breadcrumbs"]//li[position()>1]//text()',
#             as_list=True)
#         parser.add_css_rule(
#             'last_updated_date', 'span.prf-rw__date::text', regex=r': (.*)')
#         parser.add_css_rule(
#             'company', 'h1::text')
#         page_data = parser.parse()

#         breadcrumbs = page_data.pop('breadcrumbs')  # We don't need to store it
#         firebase_nodes = breadcrumbs + [page_data['company'], ]

#         for review in reviews:
#             # Review related parse
#             parser = Parser(review)

#             parser.add_css_rule(
#                 'stars',
#                 'div.stars-rating[data-rating]::attr(data-rating)')

#             parser.add_css_rule(
#                 'rating_update',
#                 'span.review-header-status__rating-label::text')

#             parser.add_css_rule(
#                 'review',
#                 '.review-body__text > p::text',
#                 as_list=True)

#             parser.add_css_rule(
#                 'reviewer',
#                 'span.review-author__info-name::text')

#             parser.add_css_rule(
#                 'helpful',
#                 '.review-footer__helpful-count > strong::text',
#                 regex=r'(\d+)')

#             parser.add_css_rule(
#                 'original_review_date',
#                 '.review-body__original-date::text',
#                 regex=r'(\w+\.? \d{1,2}, \d{4})')

#             parser.add_css_rule(
#                 'reviewer_image',
#                 '.review-author > img::attr(data-src)')

#             parser.add_css_rule(
#                 'is_verified',
#                 '.review-author__info-verified--reviewer::text')

#             parser.add_css_rule(
#                 'verified_buyer',
#                 '.review-author__info-verified--buyer::text')

#             parser.add_css_rule(
#                 'customer_response_date',
#                 '.review-body__consumer-response > span::text',
#                 regex=r'(\w+\.? \d{1,2}, \d{4})')

#             parser.add_css_rule(
#                 'customer_response_text',
#                 '.review-body__consumer-response > p::text',
#                 as_list=True)

#             parser.add_css_rule(
#                 'company_response_date',
#                 '.review-company-response__author > time::attr(datetime)')

#             parser.add_css_rule(
#                 'company_response_text',
#                 '.review-company-response__text *::text',
#                 as_list=True)

#             parser.add_css_rule(
#                 'resolution_in_progress',
#                 '.review-header-status__rating-label--in-progress::text')

#             parser.add_xpath_rule(
#                 'id',
#                 './/@data-id'
#             )

#             parsed = parser.parse()
#             parsed.update(page_data)  # Add to each review the page's data
#             parsed['short_url'] = short_url
#             self.parsed_data.append(parsed)
#             yield parsed
#         self.to_firebase('id', firebase_nodes)
#         # return self.parsed_data

if __name__ == '__main__':
    # TODO: Only for debugging; remove afterwards.
    from pprint import pprint as pp
    reviews, errors = fetch_reviews(
        'https://www.consumeraffairs.com/health/nordic-track-exercise-bikes.html'
    )
    pp(reviews)
    print('-' * 50)
    pp(reviews['reviews'][24])
    print('-' * 50)
    pp(reviews['company'])
