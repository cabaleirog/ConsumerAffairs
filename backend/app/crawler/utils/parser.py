# -*- coding: utf-8 -*-
import logging
import re
from enum import Enum

from dateutil import parser as date_parser

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Selector(Enum):
    """Define the selector to use"""
    css = 1
    xpath = 2


class Parser:
    """
    Helper class to extract data from a selector using either css or xpath
    selectors.
    """
    def __init__(self, selector):
        if isinstance(selector, str):
            raise TypeError('Selector needs to be an XPath or CSS selector')
        self.selector = selector
        self.css_rules = []
        self.xpath_rules = []
        self.items = {}

    def parse(self):
        """Extract all the items"""
        self._create_items_class()
        self._extract_by_css_selector()
        self._extract_by_xpath_selector()
        return self.items

    @property
    def rules(self):
        """Return both CSS and XPath rules"""
        return self.css_rules + self.xpath_rules

    def css(self, name, selector_string, regex=None, as_list=False):
        """Add a rule which uses CSS selector"""
        self._add_rule('css', name, selector_string, regex, as_list)

    def xpath(self, name, selector_string, regex=None, as_list=False):
        """Add a rule which uses XPath selector"""
        self._add_rule('xpath', name, selector_string, regex, as_list)

    def _add_rule(self, rule_type, name, selector_string, regex, as_list):
        if regex:
            regex = re.compile(regex)
        rules = getattr(self, '%s_rules' % rule_type)
        rules.append({
            'name': name,
            'selector_string': selector_string,
            'regex': regex,
            'as_list': as_list,
        })

    def _create_items_class(self):
        # TODO: Create items as scrapy items
        field_dict = {}
        for rule in self.rules:
            field_dict[rule['name']] = {}
        self.items = field_dict

    def _extract_by_css_selector(self):
        self._extract_by_selector(self.css_rules, Selector.css)

    def _extract_by_xpath_selector(self):
        self._extract_by_selector(self.xpath_rules, Selector.xpath)

    def _extract_by_selector(self, rules, selector):
        date_pattern = re.compile(r'_date(time)?$')
        for rule in rules:
            key = rule.get('name')
            as_list = rule.get('as_list')
            regex = rule.get('regex')

            if selector == Selector.css:
                data = self.selector.css(rule['selector_string']).extract()
            else:
                data = self.selector.xpath(rule['selector_string']).extract()

            if not data:
                self.items[key] = None
            else:
                # FIXME: Fails to capture multiple objects if as_list is False
                if as_list:
                    self.items[key] = [self.clean_text(x) for x in data]
                # TODO: Refactor this method (DRY!)
                if regex and as_list:
                        for idx, value in enumerate(self.items[key]):
                            self.items[key][idx] = self.regex(regex, value)
                if not as_list:
                    if regex:
                        data[0] = self.regex(regex, data[0])
                    self.items[key] = self.clean_text(data[0])

            if self.items[key] and date_pattern.search(key):
                # Attempt to convert dates of keys ending on _date or _datetime
                dt_value = self.items[key]
                try:
                    self.items[key] = date_parser.parse(dt_value).isoformat()
                except ValueError:
                    logger.warning('Unable to parse date on "%s"', dt_value)

    @staticmethod
    def regex(pattern, value):
        """Use the pattern to extract the data from a selector's extracted
        information.

        The specified pattern must contain exactly one parenthesized subgroup.
        """
        # TODO: Handle all values, not only the first one in the list
        match = pattern.search(value)
        if match is None:
            # Not finding a match might indicate an unhandled case which should
            # be reviewed. If a pattern is provided, a match is always expected
            msg = '%s did not find a match on string "%s"'
            logger.warning(msg, pattern, value)
            return None
        return match.group(1)

    @staticmethod
    def clean_text(value):
        """Remove spaces and line breaks from the text"""
        if value and isinstance(value, str):
            value = ' '.join(value.splitlines()).strip()
        return value

    def __add__(self, other):
        """Add the rules of both parser objects"""
        #import copy
        #new = copy.deepcopy(self)
        # css_rules = other.css_rules
        # xpath_rules = other.xpath_rules
        # items = other.items
        self.css_rules.extend(other.css_rules)
        self.xpath_rules.extend(other.xpath_rules)
        # TODO: Check for duplicated keys and raise if values are not the same.
        self.items.update(other.items)
        return self
