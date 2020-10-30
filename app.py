from flask import Blueprint
from flask_restful import Api
from resources.services import ProductList, Products


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(ProductList, '/v1/products')
api.add_resource(Products, '/v1/products/<product_id>')


