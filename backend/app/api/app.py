# -*- coding: utf-8 -*-

# import json
import logging
# import os
# from contextlib import suppress
# from subprocess import CalledProcessError, check_call

import flask
from flask import Flask, request
from flask_cors import CORS
from flask_restplus import Api, Resource, fields
# from bson.json_util import dumps
from pymongo import MongoClient

from app.crawler import fetch_categories, fetch_sub_categories, fetch_reviews
# from app.crawler.spiders.reviews import fetch_reviews
from app.crawler.spiders.companies import fetch_companies

from .decorators import timer
# from .decorators import crawler_to_json, timer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='.... Api', description='An Api for ....')

subcategory_model = api.model('subcategory', {
    'name': fields.String('Name of ........'),
    'url': fields.String('Name of ........'),
})

category_model = api.model('category', {
    'name': fields.String('Name of ........'),
    'description': fields.String('Name of ........'),
    'url': fields.String('Name of ........'),
    'subcategories': fields.List(fields.Nested(subcategory_model)),
})

company_model = api.model('company', {
    'id': fields.Integer(description='Name of ........campaons'),
    'name': fields.String(description='Name of ........'),
    'description': fields.String(description='Name of ........description'),
    'url': fields.String(description='Name of ........url'),
    'image': fields.String(description='Name of ........image'),
    'reviews': fields.Integer(default=0, description='Name of .......reviews'),
    'rating': fields.Float(description='Name of ........rating'),
})

# client = MongoClient(os.environ['CONSUMERAFFAIRS_DB_1_PORT_27017_TCP_ADDR'], 27017)
client = MongoClient('mongodb://mongo-server:27017')
db = client.consumeraffairs_db
print(db)


# @app.route("/categories")
# @timer
# @crawler_to_json
# def categories():
#     """Categories Endpoint"""
#     return fetch_website_data('categories')

@api.route('/api/v1/categories')
class Categories(Resource):
    """Categories Endpoint"""

    @api.marshal_with(category_model, envelope='data')
    def get(self):
        categories = fetch_categories()
        return categories, 200


@api.route('/api/v1/companies')
class Companies(Resource):
    """Companies Endpoint"""

    @api.marshal_with(company_model, skip_none=True, envelope='data')
    def get(self):
        subcategory_url = request.values.get('url')
        companies = fetch_companies(subcategory_url)
        return companies, 200


@api.route('/api/v1/reviews')
class Reviews(Resource):
    """Reviews Endpoint."""
    def get(self):
        url = request.args.get('url')
        page = request.args.get('page', 1)
        reviews = fetch_reviews(url, page)
        return reviews, 200


# @app.route('/api/v1/reviews/<category>/<company>')
# @timer
# def reviews_v1(category, company):
#     """Reviews Endpoint."""
#     page = request.args.get('page', 1)
#     reviews, errors = fetch_reviews(category, company + '.html', page=page)
#     return flask.jsonify(reviews)


@app.route('/api/v1/sub-categories', methods=['GET', 'POST'])
@timer
def subcategories_v1():
    """Sub-Categories Endpoint"""
    category_url = request.values.get('category_url')
    errors = []
    if not category_url:
        subcategories = []
        errors.append("Missing 'category_url'")
    else:
        subcategories = fetch_sub_categories(category_url)
    return flask.jsonify(subcategories)


# @app.route('/db/categories', methods=['GET'])
# def categories_from_db():
#     """Categories Endpoint using database"""
#     _items = db.categories.find()
#     return dumps(_items)


# @app.route('/db/categories/add', methods=['GET', 'POST'])
# def categories_from_db_add():
#     """ """
#     item = {
#         'category': '3D Printers',
#         'short_url': 'computers/3d-printer',
#         'url': 'https://www.consumeraffairs.com/computers/3d-printer/'
#     }
#     db.categories.insert_one(item)
#     docs = db.categories.find({'category': '3D Printers'})
#     print(docs)
#     return dumps({'results': docs})


# @app.route("/reviews")
# @timer
# @crawler_to_json
# def reviews():
#     """Reviews Endpoint"""
#     return fetch_website_data('reviews')


# @app.route('/companies')
# @timer
# @crawler_to_json
# def companies():
#     """Companies Endpoint"""
#     return fetch_website_data('companies')


# @app.route('/all')
# @timer
# @crawler_to_json
# def all_reviews():
#     """... Endpoint"""
#     return fetch_website_data('all_reviews')


# def fetch_website_data(crawler, all_pages=False):
#     """
#     Executes a particular crawler, returning the data fetched from the website.
#     """
#     if not isinstance(crawler, str):
#         raise TypeError('Expected string, {} provided.'.format(type(crawler)))

#     file_name = '{}.json'.format(crawler)
#     with suppress(FileNotFoundError):
#         os.remove(file_name)

#     pamars = request.args.to_dict()
#     pamars.update({'all_pages': all_pages})
#     logger.debug('Request args: %s', request.args)

#     crawl('{}_crawler'.format(crawler), file_name, **pamars)

#     try:
#         with open(file_name, 'r', encoding='utf-8') as file_name:
#             return file_name.readlines()
#     except FileNotFoundError as error:
#         logger.critical("Spider <%s> didn't save json output file.", crawler)
#         return error


# def crawl(crawler_name, json_file, **url_params):
#     """
#     Executes the crawler as a subprocess, waiting for the process to complete
#     before returning the output.
#     """
#     parameters = ['scrapy', 'crawl', crawler_name, '-o', json_file]
#     for key, value in iter(url_params.items()):
#         logger.debug('Adding query param %s=%s to the crawler', key, value)
#         parameters.extend(['-a', '{}={}'.format(key, value)])
#         logger.debug('Running command "%s"', ' '.join(parameters))
#     try:
#         check_call(parameters)
#     except CalledProcessError:
#         logger.error('Unable to complete the crawl')
