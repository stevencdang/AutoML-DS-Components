
# Author: Steven C. Dang

# MongoDB interface DataExplorer DB

import logging
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

from ls_dataset.d3m_dataset import D3MDataset

logger = logging.getLogger(__name__)

class DXDB(object):

    tbls = {
            'ds_metadata': 'Datasets'
    }
    
    def __init__(self, db_url):
        self.db = MongoClient("mongodb://%s" % db_url)['dexplorer']
        

    def insert_dataset_metadata(self, ds):
        # ds is a ls_dataset
        d = json.loads(ds.to_json())
        did = self.db[self.tbls['ds_metadata']].insert_one(d).inserted_id
        return did
        

    def get_dataset_metadata(self, dsid=None):
        if dsid is None:
            ds_json = self.db[self.tbls['ds_metadata']].find_one()
        else:
            ds_json = self.db[self.tbls['ds_metadata']].find_one({'_id': ObjectId(dsid)})
        return D3MDataset.from_json(ds_json)

        


