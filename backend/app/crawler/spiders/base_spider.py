# -*- coding: utf-8 -*-
"""Base class for ConsumerAffairs's spiders"""
from urllib.parse import urlencode, urljoin
import os
import logging

#import firebase_admin as fba
import scrapy
from firebase_admin import credentials, db, initialize_app, get_app

from ...api.decorators import timer

logger = logging.getLogger(__name__)


class BaseSpider(scrapy.Spider):
    """Base class for spiders. All spiders must inherit from this class.

    Keyword Arguments:
        url (str): Short url excluding the base site url.
        all_pages (bool): Should the spider crawl all pages (default: False).
        page (int): The page to crawl from pages with pagination (default: 1).

    """
    def __init__(self, *args, **kwargs):
        self.parsed_data = []

        self.start_urls = self.start_urls[:1]

        # Initialize Firebase
        self.firebase = self._get_firebase_app()

        url_to_append = kwargs.pop('url', None)
        if url_to_append:
            self.start_urls[0] = urljoin(self.start_urls[0], url_to_append)

        # Always be nice to the server if crawling more than 1 page
        all_pages = kwargs.pop('all_pages', False)
        if all_pages:
            pass
            # self.download_delay = 1.5

        if kwargs:
            self.start_urls = ['{}?{}'.format(
                self.start_urls[0],
                urlencode(kwargs),
            )]
        logger.debug('Initialize URL: %s' % self.start_urls)
        super().__init__(*args, **kwargs)

    def parse(self, response):
        raise NotImplementedError

    def _get_firebase_app(self):
        try:
            self._firebase = get_app(self.name)
        except ValueError:
            if not getattr(self, '_firebase', None):
                cred = credentials.Certificate(
                    '{}/app/crawler/ConsumerAffairs-14166b9c2a4d.json'.format(os.getcwd()))
                self._firebase = initialize_app(
                    cred,
                    {'databaseURL': 'https://consumeraffairs-clone.firebaseio.com/'},
                    self.name
                )
        return self._firebase

    # def to_firebase(self, identifier, group_name='', data=None):
    # @timer
    def to_firebase(self, identifier, child_node=''):
        ref = db.reference(self.name, self.firebase)
        data_dict = {x[identifier]: x for x in self.parsed_data}
        if isinstance(child_node, list):
            for node in child_node:
                ref = ref.child(node)
            ref.update(data_dict)
        else:
            ref.child(child_node).update(data_dict)
