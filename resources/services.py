import json
from flask_restful import Resource
from flask import request, jsonify
from pymongo import MongoClient
from bson import json_util
import urllib.parse
from pymongo.errors import ServerSelectionTimeoutError
from config import Config

db = Config()
collection = db.collection
# username = urllib.parse.quote_plus('somesh')
# password = urllib.parse.quote_plus('eEwAodimXBOi3liX')
#
#
# uri = "mongodb+srv://%s:%s@cluster0.rxcrr.mongodb.net/my_database?retryWrites=true&w=majority" % (username, password)
# client = MongoClient(uri)
# db = client["my_database"]
# collection = db["my_collection"]

class ProductList(Resource):
    def get(self):
        """Returns list of products."""
        all_products = list(collection.find({}))
        return json.dumps(all_products, default=json_util.default), 200

    def post(self):
        """Creates a new product"""
        invalid = False
        request_payload = request.json  # if the key doesnt exist, it will return a None
        product = request_payload
        existing_product = list(collection.find({"product_id": product["product_id"]}))
        if request.method != "POST" and "product_id" not in product:
            invalid = True
        elif existing_product:
            return conflict()
        elif invalid:
            return invalid_input()
        else:
            collection.insert_one(product)
        return product, 201


class Products(Resource):
    def put(self, product_id):
        """Updates the product details for given product id ."""
        request_payload = request.json  # if the key doesnt exist, it will return a None
        product = request_payload
        existing_product = list(collection.find({"product_id": product_id}))
        invalid = False
        my_query = existing_product[0]
        new_value = {"$set": product}
        if invalid:
            return invalid_input()
        elif existing_product:
            collection.update_one(my_query, new_value)
        else:
            collection.insert_one(product)
        return product, 200

def invalid_input(error=None):
    message = {
        'status': 405,
        'message': "Invalid Input"
    }
    resp = jsonify(message)
    resp.status_code = 405
    return resp


def conflict(error=None):
    message = {
        'status': 409,
        'message': "Product already exists"
    }
    resp = jsonify(message)
    resp.status_code = 409
    return resp

