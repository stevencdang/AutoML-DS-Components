from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

from ls_dataset.d3m_dataset import D3MDatset



app = Flask(__name__)
CORS(app)
db_client = MongoClient('localhost', 27017,
                     username="root", password="lsadmin")

def hello_world():
    db = db_client['dexplorer']
    ds_col = db['Datasets']
    dataset = ds_col.find_one()
    dataset['_id'] = str(dataset['_id'])
    print(dataset)
    # return json.dumps({"result": "Hello World"})
    return json.dumps(dataset)


@app.route('/')
def get_dataset():
    dsid = "5cb40d490d80e10621bc813f"
    db = db_client['dexplorer']
    ds_col = db['Datasets']
    dataset = ds_col.find_one()
    print(dataset)
    dataset = ds_col.find_one({"_id": ObjectId(str(dataset['_id']))})
    print(dataset)
    dataset['_id'] = str(dataset['_id'])
    return json.dumps({"result": "Hello World"})
    # return json.dumps(dataset)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
