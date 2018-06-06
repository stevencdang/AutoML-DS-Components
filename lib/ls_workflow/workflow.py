
# Author: Steven C. Dang

# Class representing an ordered set of operations on a given data input

import logging
import json

from google.protobuf import json_format

from d3m_ta2.api_v3 import pipeline_pb2

logger = logging.getLogger(__name__)



class Workflow(object):

    def __init__(self, wid, model=None, scores=None, fit=None):
        self.id = wid
        self.model = model
        self.steps = None
        self.scores = scores
        self.fit = fit
    
    def add_description(self, model, step_desc):
        self.model = model
        self.steps = step_desc

    def get_default_output(self):
        """
        Just returns the first output

        """
        return self.model.outputs[0].name

    def __str__(self):
        out = json_format.MessageToJson(self.model)
        return out

    @staticmethod
    def from_json(data):
        """
        Load from json string

        """
        logger.debug("type of data to load from json: %s" % str(type(data)))
        if isinstance(data, str):
            d = json.loads(data)
            logger.debug(d)
            d = json_format.Parse(data, pipeline_pb2.PipelineDescription())
        elif isinstance(data, dict):
            logger.debug(data)
            d = json_format.Parse(str(data), pipeline_pb2.PipelineDescription())
        else:
            raise Exception("Invalid type given: %s" % str(type(data)))
        
        out = Workflow(d.id, d)
        logger.debug("Got pipeline parsed: %s" % str(d))
        return out



    def to_file(self, fpath):
        """
        Writes the workflows to a file where the first line is tab separated
        list of solution ids. The second row contains a stringified version
        of the json for the corresponding solution id

        """
        return fpath


