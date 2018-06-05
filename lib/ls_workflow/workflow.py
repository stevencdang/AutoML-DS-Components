
# Author: Steven C. Dang

# Class representing an ordered set of operations on a given data input

import logging

from google.protobuf import json_format

logger = logging.getLogger(__name__)



class Workflow(object):

    def __init__(self, wid):
        self.id = wid
        self.model = None
        self.steps = None
        self.scores = None
        self.fit = None
    
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

    def to_file(self, fpath):
        """
        Writes the workflows to a file where the first line is tab separated
        list of solution ids. The second row contains a stringified version
        of the json for the corresponding solution id

        """
        return fpath


