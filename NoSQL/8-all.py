#!/usr/bin/env python3

"""8. List all documents in Python"""


def list_all(mongo_collection):
    """list all docs in a collection"""
    return mongo_collection.find()
