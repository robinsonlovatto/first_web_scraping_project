import pandas as pd
import os
from pymongo import MongoClient

class MongoConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._client = None
            cls._instance._db = None
            cls._instance._collection = None
        return cls._instance

    def __init__(self, host='localhost', port=27017, database='test', collection='data'):
        if self._client is None:
            self.host = os.getenv("MONGO_HOST", host)
            self.port = int(os.getenv("MONGO_PORT",port))
            self.database_name = os.getenv("MONGO_DATABASE",database)
            self.collection_name = os.getenv("MONGO_COLLECTION",collection)
            self._connect()

    def _connect(self):
        self._client = MongoClient(self.host, self.port)
        self._db = self._client[self.database_name]
        self._collection = self._db[self.collection_name]

    def save_dataframe(self, df):
        # converts the dataframe to json
        data = df.to_dict(orient='records')
        # inserting in the mongodb collection
        self._collection.insert_many(data)
        print("DataFrame saved on MongoDB succesfully.")

    def close_connection(self):
        if self._client:
            self._client.close()
            print("Connection closed succesfully.")