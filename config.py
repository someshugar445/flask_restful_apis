from pymongo import MongoClient

import urllib.parse
from pymongo.errors import ServerSelectionTimeoutError

username = urllib.parse.quote_plus('somesh')
password = urllib.parse.quote_plus('eEwAodimXBOi3liX')


class Config():
    uri = "mongodb+srv://%s:%s@cluster0.rxcrr.mongodb.net/my_database?retryWrites=true&w=majority" % (username, password)
    client = MongoClient(uri)

    db = client["my_database"]
    collection = db["my_collection"]
    try:
        info = client.server_info()  # Forces a call.
    except ServerSelectionTimeoutError:
        print("server is down.")
