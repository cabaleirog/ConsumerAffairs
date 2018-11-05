# -*- coding: utf-8 -*-
"""Decorators for Endpoint functions."""

import json
import logging
import time
from functools import wraps

from flask import jsonify

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def crawler_to_json(func):
    """
    Decorator for converting data saved by the crawler into a json response.
    """
    @wraps(func)
    def _wrapper(*args, **kwargs):
        data = []
        errors = []
        response = func(*args, **kwargs)

        if isinstance(response, FileNotFoundError):
            errors.append('Crawler failed to fetch requested information.')
            response = None
        if response:
            data = json.loads(''.join([x.strip() for x in response]))

        return jsonify({
            'result_count': len(data),
            'results': data,
            'errors': errors,
        })

    return _wrapper


def timer(func):
    """Simple decorator to log execution time of the wrapped method"""
    @wraps(func)
    def _wrapper(*args, **kwargs):
        initial_time = time.time()
        returned_value = func(*args, **kwargs)
        logger.info(
            'Method <%s> of <%s> took %.3f seconds.',
            func.__qualname__,
            func.__module__,
            time.time() - initial_time,
        )
        return returned_value
    return _wrapper
