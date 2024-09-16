#!/usr/bin/env python3

"""12. Log stats"""


from pymongo import MongoClient


# Connect to MongoDB
client = MongoClient()
db = client.logs
collection = db.nginx

# Get the total number of documents in the collection
total_logs = collection.count_documents({})

# Print the number of logs
print(f"{total_logs} logs where {total_logs} is the number of documents in this collection")

# Get the number of documents with each method
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
method_counts = [collection.count_documents({"method": method}) for method in methods]

# Print the number of documents with each method
print("Methods:")
for method, count in zip(methods, method_counts):
    print(f"\t{count} {method}")

# Get the number of documents with method=GET and path=/status
get_status_count = collection.count_documents({"method": "GET", "path": "/status"})

# Print the number of documents with method=GET and path=/status
print(f"{get_status_count} logs where method=GET and path=/status")