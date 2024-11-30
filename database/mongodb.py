from pymongo import MongoClient


def get_mongodb_client(uri='mongodb://localhost:27017'):
    return MongoClient(uri)