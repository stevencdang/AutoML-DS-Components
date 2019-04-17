from pymongo import MongoClient
import json


client = MongoClient('localhost', 27017,
                     username="root", password="lsadmin")


# Open sample dataset.json
fpath = "datasetDoc.json"
with open(fpath, 'r') as f:
    ds_json = json.load(f)
print("Dataset json")
print(ds_json)

db = client['dexplorer']
ds_col = db["Datasets"]
ds_id = ds_col.insert_one(ds_json).inserted_id
print("Added datset. assigned id: %s" % ds_id)

print("list of all collections in db 'dexplorer'")
for col in db.collection_names():
    print(col)

# default collections in dexplorer database
collections = [
    "Datasets",
    "SimpleEDASessions",
    "EDAStats"
]

print("Initializing collections in db")
for col in collections:
    print(col)
    next_col = db[col]

print("list of all collections in db 'dexplorer'")
for col in db.collection_names():
    print(col)

