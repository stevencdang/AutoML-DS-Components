from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

from ls_dataset.d3m_dataset import D3MDataset
from dxdb.dx_db import DXDB



app = Flask(__name__)
CORS(app)
db_client = DXDB('localhost:27017')


@app.route('/')
def main():
    return "Hello World"

@app.route('/ds/getDataset')
def get_dataset():

    ds = db_client.get_dataset_metadata()
    print([str(d) for d in ds.get_data_columns()])
    # return json.dumps({"result": "Hello World"})
    return ds.to_json()

@app.route('/ds/getDataCols')
def get_data_columns():
    """
    Return a list of the data columns for each data resource in the dataset

    """
    ds = db_client.get_dataset_metadata()
    result = {'DatasetId': ds.id,
              'DatasetColumns': [d.to_json() for d in ds.get_data_columns()]
    }

    print(result)
    # return result
    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
