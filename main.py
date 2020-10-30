from flask import Flask
from flask import request, jsonify
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
import urllib.parse
from pymongo.errors import ConnectionFailure
from pymongo.errors import ServerSelectionTimeoutError
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


username = urllib.parse.quote_plus('somesh')
password = urllib.parse.quote_plus('eEwAodimXBOi3liX')

uri = "mongodb+srv://%s:%s@cluster0.rxcrr.mongodb.net/my_database?retryWrites=true&w=majority" % (username, password )
client = MongoClient(uri)

db = client["my_database"]
collection = db["my_collection"]
try:
    info = client.server_info() # Forces a call.
except ServerSelectionTimeoutError:
    print("server is down.")


class ProductList(Resource):
    def get(self):
        all_products = list(collection.find({}))
        return json.dumps(all_products, default=json_util.default), 200

    def post(self):
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
        return product,201

class Products(Resource):
    def put(self,product_id):
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
        return product,200


api.add_resource(ProductList, '/api/v1/products')
api.add_resource(Products, '/api/v1/products/<product_id>')

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


if __name__ == "__main__":
    app.run(debug=True, port=5000)
