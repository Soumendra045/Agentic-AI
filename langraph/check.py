from pymongo import MongoClient

client = MongoClient("mongodb://admin:admin@localhost:27018/?authSource=admin")
client.admin.command('ping')
print("✅ Connected!")