import uuid
import yaml
from datetime import datetime
from pymongo import MongoClient

class MongoDBConfig():
    def load_config(self, config_path:str):
        config_file = open(config_path, 'r')
        config = yaml.load(config_file, yaml.SafeLoader)
        return config

    def __init__(self, config_yaml_path):
        self.config = self.load_config(config_yaml_path)
        self.client = MongoClient(self.config['mongo_client'])
        self.db = self.client[self.config['database_name']]
        self.collection = self.db[self.config['collection_name']]
    
    def insert_one(self, data):
        query = {
            '_id': uuid.uuid4().hex,
            'location': data['location'],
            'text': data['text'],
            'rating': data['rating'],
            'datetime': data['datetime'],
            'scrapped_at': str(datetime.now())[:19]
        }

        self.collection.insert_one(query)
    
    def delete_all(self):
        return self.collection.delete_many({})
    
    def update_one(self, _id:str, done_at:str=None, vid:str=None, transcript:str=None):
        query = { '_id': _id }

        if done_at is None:
            if vid is None:
                newvalue = { '$set': {'transcript': transcript} }
            elif transcript is None:
                newvalue = { '$set': {'vid': vid} }
        else:
            newvalue = { '$set': {'done_at': done_at} }

        return self.collection.update_one(query, newvalue)

    def find_one(self, _id:str):
        query = { '_id': _id }
        return self.collection.find_one(query)
    
    def find_all(self, skip:int=0, limit:int=100):
        return list(self.collection.find().limit(limit))
    
    def count_data(self, query):
        return len(list(self.collection.find(query)))