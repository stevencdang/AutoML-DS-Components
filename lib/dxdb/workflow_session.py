
# Author: Steven C. Dang

# MongoDB interface DataExplorer DB

import logging
import inspect

from ls_iviz.simple_eda import *


logger = logging.getLogger(__name__)

class WorkflowSession(object):
    
    available_states = ['Not Ready']
    
    def __init__(self, 
                 user_id, 
                 workflow_id, 
                 comp_id, 
                 comp_type, 
                 _id=None, 
                 state=None,
                 session_url=None
                 ):
        if _id is not None:
            self._id = _id
        self.user_id = user_id
        self.workflow_id = workflow_id
        self.comp_type = comp_type
        self.comp_id = comp_id
        self.session_url = session_url
        if state is None:
            self.state = self.available_states[0]
        else:
            self.state = state

    def to_json(self):
        logger.debug("Type of self: %s" % str(type(self)))
        return json.dumps(self, default=lambda o: o.__dict__, 
                                      sort_keys=True, indent=4)

    @staticmethod
    def from_json(ses_json): 
        logger.debug("Initializing WorkflowSession from json: %s" % str(ses_json))
        if ses_json['comp_type'].lower() == "datasetimporter":
            logger.debug("initializing a dataset importer session")
            ses = ImportDatasetSession(**ses_json)
        elif  ses_json['comp_type'].lower() == "simpleedasession":
            logger.debug("initializing a simple eda session")
            ses = SimpleEDASession(**ses_json)
        else:
            raise Exception("Unable to identify class to initialize workflow session with session: %s" % str(ses_json))
        return ses
        # if issubclass(cls, WorkflowSession):
            # ses = cls(**ses_json)
            # return ses
        # else:
            # raise Exception("Invalid class given: %s" % str(cls))

    def set_session_url(self, url):
        self.session_url = url

    def get_possible_states(self):
        return self.available_states
        

class SimpleEDASession(WorkflowSession):

    dataset_id = None

    def __init__(self, userId, workflowId, compType, session_url=None, dataset=None):
        if dataset is not None:
            self.dataset_id = dataset._id
        super().__init__(userId, workflowId, compType, session_url)
        self.visualizations = []

    def set_dataset(self, dataset):
        self.dataset_id = dataset._id

    def add_viz(self, viz):
        v_ids = set(self.visualizations)
        if viz._id not in v_ids:
            self.visualizations.append(viz._id)

    @classmethod
    def from_json(cls, ses_json): 
        logger.debug("Initializing SimpleEDASession from json: %s" % str(ses_json))
        ses = cls(ses_json['user_id'], ses_json['workflow_id'],
                         ses_json['component_type'], ses_json['session_url'],
        )
        ses.dataset_id = ses_json['dataset_id']
        for vizid in ses_json['visualizations']:
             logger.debug("Adding visualization id to eda session: %s" % vizid)
             ses.visualizations.append(vizid)
        return ses

class ImportDatasetSession(WorkflowSession):

    available_states = ['Not Ready', 
                        'No Dataset Imported',
                        'Dataset Imported'
                        ]
    def __init__(self, 
                 user_id, 
                 workflow_id, 
                 comp_id, 
                 comp_type, 
                 _id=None, 
                 state=None,
                 dataset_id=None,
                 available_datasets=None,
                 session_url=None):
        super().__init__(user_id, workflow_id, 
                         comp_id, comp_type, 
                         _id, session_url)
        self.dataset_id = dataset_id
        if available_datasets is None:
            self.available_datasets = []
        else:
            self.available_datasets = available_datasets
        if state is None:
            self.state = self.available_states[0]
        else:
            self.state = state

    def set_state_ready(self):
        self.state = self.available_states[1]

    def set_state_complete(self):
        self.state = self.available_states[2]

    def set_dataset_id(self, dataset_id):
        logger.info("Setting session dataset id: %s" % dataset_id)
        self.dataset_id = dataset_id

    def set_available_dataset_ids(self, datasets):
        # Takes a list of dataset IDs
        self.available_datasets = datasets

    def get_available_dataset_ids(self):
        return self.available_datasets
    

