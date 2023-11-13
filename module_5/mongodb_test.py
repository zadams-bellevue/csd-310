#!/usr/bin/env python3

"""MongoDB connection test"""

from pymongo import MongoClient

URL = "mongodb+srv://admin:admin@cluster0.uvpueeb.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(URL)
db = client.pytech

print("-- Pytech COllection List --") # (typo in assignment instructions)
print(db.list_collection_names())
