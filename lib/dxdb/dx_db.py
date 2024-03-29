
# Author: Steven C. Dang

# MongoDB interface DataExplorer DB

import logging
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

from ls_dataset.d3m_dataset import D3MDataset
from ls_problem_desc.ls_problem import ProblemDesc
from dxdb.workflow_session import *

logger = logging.getLogger(__name__)

class DXDB(object):

    tbls = {
            'ds_metadata': 'Datasets',
            'problems': 'Problems',
            'wf_sessions': 'WorkflowSessions',
            'viz_sessions': 'VizSessions',
            'solutions': "Solutions",
            'fitted_solutions': "FittedSolutions",
            'predictions': "Predictions",
            'model_scores': "ModelScores",
            'ranked_models': "RankedModels"
    }
    
    def __init__(self, db_url):
        logger.debug("Connecting to mongo at: %s" % ("mongodb://%s" % db_url))
        self.db = MongoClient("mongodb://%s" % db_url)['dexplorer']

    def list_all_collections(self):
        logger.info("Getting list of all collections in db")
        result = self.db.list_collection_names()
        logger.debug("Got %i collection names from db" % len(result))
        return result

    def get_all_datasets(self):
        logger.info("Call pymongo collections" )
        logger.info(self.db.list_collection_names())
        logger.info("Retrieving all datasets from db")
        results = self.db[self.tbls['ds_metadata']].find()
        logger.debug("Retrieved %i datasets from db" % results.count())
        return results
        

    def insert_dataset_metadata(self, ds):
        # ds is a ls_dataset
        logger.info("Inserting dataset to db: %s" % ds.id)
        logger.debug("Loading dataset to json")
        d = json.loads(ds.to_json())
        logger.debug("Loaded dataset to json: %s" % str(d))
        did = self.db[self.tbls['ds_metadata']].insert_one(d).inserted_id
        return did

    def has_dataset(self, ds):
        # Check if a given dataset metadata is already within the db
        if ds._id is not None:
            logger.debug("dataset already has _id defined. Querying using _id: %s" % ds._id)
            results = self.db[self.tbls['ds_metadata']].find({'_id': ObjectId(ds._id)})
            if results.count() > 0:
                logger.debug("Dataset is in db")
                return True
        logger.debug("checking db for dataset with id: %s" % ds.id)
        results = self.db[self.tbls['ds_metadata']].find({'about.datasetID': ds.id})
        if results.count() > 0:
            logger.debug("Dataset is in db")
            return True
        else:
            logger.debug("Dataset is not in db")
            return False

    def get_dataset_with_name(self, name=None):
        logger.debug("looking up dataset with name: %s" % name)
        if name is None:
            ds_json = self.db[self.tbls['ds_metadata']].find_one()
        else:
            ds_json = self.db[self.tbls['ds_metadata']].find_one({'about.datasetID': name})
        # Convert _id to string
        ds_json['_id'] = str(ds_json['_id'])
        logger.debug("Got dataset: %s" % str(ds_json)[:400])
        return D3MDataset.from_json(ds_json)

    def get_dataset_metadata(self, dsid=None):
        logger.debug("looking up dataset with id: %s" % dsid)
        if dsid is None:
            ds_json = self.db[self.tbls['ds_metadata']].find_one()
        else:
            ds_json = self.db[self.tbls['ds_metadata']].find_one({'_id': ObjectId(dsid)})
        # Converting returned ObjectID to string
        ds_json['_id'] = str(ds_json['_id'])
        return D3MDataset.from_json(ds_json)

    def get_problem(self, pid=None):
        logger.debug("looking up problem with id: %s" % pid)
        if pid is None:
            ds_json = self.db[self.tbls['problems']].find_one()
        else:
            ds_json = self.db[self.tbls['problems']].find_one({'_id': ObjectId(pid)})
        return ProblemDesc.from_json(ds_json)

    def insert_problem(self, prob):
        logger.info("Inserting problem to db: %s" % prob.name)
        logger.debug("Loading problem to json")
        d = json.loads(prob.to_json())
        logger.debug("Loaded problem to json: %s" % str(d))
        pid = self.db[self.tbls['problems']].insert_one(d).inserted_id
        logger.debug("Got problem id: %s" % pid)
        return str(pid)

    def replace_problem(self, pid, prob):
        logger.info("Replacing problem in db with given problem with id: %s" % pid)
        # prob._id = ObjectId(prob._id)
        d = json.loads(prob.to_json())
        if '_id' in d.keys():
            logger.debug("Found _id in problem. Removing to not overwrite")
            del(d['_id'])
        logger.debug("Loaded problem to json: %s" % str(d))
        result = self.db[self.tbls['problems']].replace_one(
            {'_id': ObjectId(pid)},
            d
        )
        logger.debug("Count of documents modified by replace operation: %i" % result.modified_count)
        return result.acknowledged

    def add_workflow_session(self, session):
        d = self.db[self.tbls['wf_sessions']].insert_one(session.__dict__)
        logger.debug("Added workflow session to db")
        logger.debug(d)
        logger.debug("getting inserted id: %s" % str(d.inserted_id))
        # did = self.db[self.tbls['wf_sessions']].insert_one(session.__dict__).inserted_id
        session._id = str(d.inserted_id)
        return session

    def get_workflow_session(self, wfid):
        logger.debug("Getting workflow session: %s" % wfid)
        wfs = self.db[self.tbls['wf_sessions']].find_one({'_id': ObjectId(wfid)})
        wfs['_id'] = str(wfs['_id'])
        logger.debug("Got workflow session: %s" % str(wfs))
        session = WorkflowSession.from_json(wfs)  
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
        did = self.db[self.tbls['viz_sessions']].insert_one(viz.as_dict()).inserted_id
        viz._id = str(did)
        logger.debug("Added visualization session to db: \n%s" % str(viz.as_dict()))
        return viz

    def get_visualizations(self, viz_ids):
        logger.debug("Searching for visualizations with ids: %s" % viz_ids)
        results = self.db[self.tbls['viz_sessions']].find({"_id": {"$in": [ObjectId(viz) for viz in viz_ids]}})
        out = [SimpleEDAViz.from_json(doc, self) for doc in results]
        logger.debug("Found matches: %s" % out)
        return out

    def add_solution(self, data):
        logger.debug("Adding given solution to db")
        d = self.db[self.tbls['solutions']].insert_one(data.__dict__)
        logger.debug("Added solution to db with id: %s" % str(d.inserted_id))
        # did = self.db[self.tbls['wf_sessions']].insert_one(session.__dict__).inserted_id
        data._id = str(d.inserted_id)
        return data

    def add_fitted_solution(self, data):
        logger.debug("Adding given fitted solution to db")
        d = self.db[self.tbls['fitted_solutions']].insert_one(data.__dict__)
        logger.debug("Added fitted solution to db with id: %s" % str(d.inserted_id))
        # did = self.db[self.tbls['wf_sessions']].insert_one(session.__dict__).inserted_id
        data._id = str(d.inserted_id)
        return data

    def insert_data(self, tbl, data):
        if tbl not in self.tbls:
            raise Exception("Invalid table given to insert data: %s\nMust specify one of: %s" % 
                            (tbl, str(list(self.tbls.values()))))
        else:
            logger.debug("Adding given data to table, %s" % self.tbls[tbl])
            # dd = data.__dict__
            dd = data.to_json()
            if '_id' in dd.keys():
                logger.warning("Found _id, %s, in data to be inserted. Removing to insert new data" % dd['_id'])
                del dd['_id']
            try:
                d = self.db[self.tbls[tbl]].insert_one(dd)
            except Exception as e:
                logger.error("Could not insert data into table %s:\n %s" % (self.tbls[tbl], str(data)))
                raise Exception("Error encountered when inserting new data into table %s. Error: %s" % 
                                (self.tbls[tbl], str(e)))
            logger.debug("Added data to table, %s,  with id: %s" % (self.tbls[tbl], str(d.inserted_id)))
            # did = self.db[self.tbls['wf_sessions']].insert_one(session.__dict__).inserted_id
            data._id = str(d.inserted_id)
            return data._id


    def update_data_fields(self, tbl, data, fields):
        if tbl not in self.tbls:
            raise Exception("Invalid table given to update data fields: %s\nMust specify one of: %s" % 
                            (tbl, str(list(self.tbls.values()))))
        else:
            logger.debug("Updating fields %s for db entry with _id, %s, in table, %s" % 
                         (str({k: v for k, v in data.__dict__.items() if k in fields }), 
                          data._id, self.tbls[tbl]))
            try:
                self.db[self.tbls[tbl]].update_one(
                        {"_id": ObjectId(data._id)},
                        {"$set": {k: v for k, v in data.__dict__.items() if k in fields }}
                        )
            except Exception as e:
                logger.error("Error while updating object: %s" % str(e))
                raise Exception("Error encountered while updating object in db table, %s. Error: %s" %
                                (self.tbls[tbl], str(e)))
    
    def get_object(self, tbl, obj_id):
        logger.debug("Getting object from table %s with id: %s" % (self.tbls[tbl], obj_id))
        try: 
            obj = self.db[self.tbls[tbl]].find_one({'_id': ObjectId(obj_id)})
        except Exception as e:
            logger.error("Error while retrieving object with _id, %s, from table %s" %
                         (obj_id, self.tbls[tbl]))
            raise Exception("Error encountered while getting object from table %s. Error: %s" %
                            (self.tbls[tbl], str(e)))
        # Convert ObjectId in _id field from mongodb to str for easier management
        obj['_id'] = str(obj['_id'])
        logger.debug("Got object from table %s: %s" % (self.tbls[tbl], str(obj)))
        return obj



