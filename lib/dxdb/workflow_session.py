
# Author: Steven C. Dang

# MongoDB interface DataExplorer DB

import logging

from ls_iviz.simple_eda import *


logger = logging.getLogger(__name__)

class WorkflowSession(object):
    
    _id = None
    user_id = None
    workflow_id = None
    component_type = None
    session_url = None

    def __init__(self, userId, workflowId, compType, session_url=None):
        self.user_id = userId
        self.workflow_id = workflowId
        self.component_type = compType
        self.session_url = session_url

    @classmethod
    def from_json(cls, ses_json): 
        logger.debug("Initializing WorkflowSession from json: %s" % str(ses_json))
        ses = cls(ses_json['user_id'], ses_json['workflow_id'],
                         ses_json['component_type'], ses_json['session_url']
        )
        return ses

    def set_session_url(self, url):
        self.session_url = url
        

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

