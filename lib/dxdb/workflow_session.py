
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

