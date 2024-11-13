import os
from os.path import join, dirname
from dotenv import load_dotenv
from pymongo import MongoClient


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class PyMongo_DB:
    def __init__(self):
        self.CONNECTION_STRING = os.environ.get("MONGODB_URI")

    def get_database(self):
        client = MongoClient(self.CONNECTION_STRING)
        return client['auth-microservice']

    def check_IP(self, IP):
        print('check ' + IP)
        db = self.get_database()
        collection = db["whitelist"]
        if collection.count_documents({
            "IP": IP,
        }):
            return True
        return False

    def insert_IP(self, IP):
        print('insert ' + IP)
        db = self.get_database()
        collection = db["whitelist"]
        data = {
            "IP": IP
        }
        collection.insert_one(data)
