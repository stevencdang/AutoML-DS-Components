
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
            'ds_metadata': 'Datasets',
            'wf_sessions': 'WorkflowSessions',
            'viz_sessions': 'VizSessions'

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

    def add_workflow_session(self, session):
        d = self.db[self.tbls['wf_sessions']].insert_one(session.__dict__)
        logger.debug("Added workflow session to db")
        logger.debug(d)
        logger.debug("getting inserted id: %s" % str(d.inserted_id))
        # did = self.db[self.tbls['wf_sessions']].insert_one(session.__dict__).inserted_id
        session._id = str(d.inserted_id)
        return session

    def update_workflow_session(self, session, fields):
        try:
            logger.debug("Updating workflow session to: %s" % str(session.__dict__))
            logger.debug("Updating fields: %s" % str({k: v for k, v in session.__dict__.items() if k in fields })) 
            self.db[self.tbls['wf_sessions']].update_one(
                    {"_id": ObjectId(session._id)},
                    {"$set": {k: v for k, v in session.__dict__.items() if k in fields }}
                    )
        except Exception as e:
            logger.error("Error while updating workflow session: %s" % str(e))

    def add_viz(self, viz):
        logger.debug(viz.to_json())
        did = self.db[self.tbls['viz_sessions']].insert_one(viz.to_json()).inserted_id
        viz._id = str(did)
        logger.debug("Added visualization session to db: \n%s" % str(viz.to_json()))
        return viz
