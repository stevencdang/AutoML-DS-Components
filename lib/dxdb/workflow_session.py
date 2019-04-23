
# Author: Steven C. Dang

# MongoDB interface DataExplorer DB

import logging


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

class SimpleEDASession(WorkflowSession):

    dataset_id = None

    def __init__(self, userId, workflowId, compType, session_url=None, dataset=None):
        if dataset is not None:
            self.dataset_id = dataset._id
        super().__init__(userId, workflowId, compType, session_url)

    def set_dataset(self, dataset):
        self.dataset_id = dataset._id

