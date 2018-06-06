
# Author: Steven C. Dang

# Class representing an ordered set of operations on a given data input

import logging
import json
from abc import ABC, abstractmethod

from google.protobuf import json_format

from d3m_ta2.api_v3 import pipeline_pb2

logger = logging.getLogger(__name__)

class Metric(object):

    __types__ = [
            'METRIC_UNDEFINED',
            'ACCURACY',
            'F1',
            'F1_MICRO',
            'F1_MACRO',
            'ROC_AUC',
            'ROC_AUC_MICRO',
            'ROC_AUC_MACRO',
            'MEAN_SQUARED_ERROR',
            'ROOT_MEAN_SQUARED_ERROR',
            'ROOT_MEAN_SQUARED_ERROR_AVG',
            'MEAN_ABSOLUTE_ERROR',
            'R_SQUARED',
            'NORMALIZED_MUTUAL_INFORMATION',
            'JACCARD_SIMILARITY_SCORE',
            'PRECISION_AT_TOP_K',
            'LOSS'
    ]

    __ignore_chars__ = ['-', '_']

    def __init__(self, my_type):
        self.type = self.get_match(my_type)

    def __eq__(self, other):
        return self.type == other.type

    def __ne__(self, other):
        return self.type != other.type

    def is_match(self, t):
        return self.get_match(t) == self.type

    def __str__(self):
        return self.type
    
    @staticmethod
    def get_types():
        types = []
        for m in Metric.__types__:
            t = m.lower()
            for char in self.__ignore_chars__:
                t.replace(char, "")
            types.append(t)
        return types

    @staticmethod
    def get_match(t):
        t = Metric.convert_type(t)
        try:
            i = Metric.get_types().index(t)
            return Metric.__types__(i)
        except ValueError:
            return None

    @staticmethod
    def convert_type(t):
        t = t.lower()
        for char in self.__ignore_chars__:
            t.replace(char, "")
        return t

    @staticmethod
    def is_valid(t):
        return Metric.convert_types(t) in Metric.get_types()

class ModelInput(object):

    def __init__(self, name):
        self.name = name

class ModelOutput(object):

    def __init__(self, name, source):
        self.name = name
        self.source = source

class ModelNode(ABC):

    @abstractmethod
    def get_type(self):
        pass

class SimpleModelNode(ModelNode):

    def __init__(self, op, args=None, outputs=None, hyperparams=None):
        self.operator = op
        if args is not None:
            self.args = args
        else:
            self.args = []
        if outputs is not None:
            self.outputs = outputs
        else:
            self.outputs = []
        if hyperparams is not None:
            self.hyperparams = hyperparams
        else:
            self.hyperparams = []
    
    def get_type(self):
        return "SimpleNode"

class SearchModelNode(ModelNode):

    def __init__(self, inputs=None, outputs=None):
        if inputs is None:
            self.inputs = None
        else:
            self.inputs = [ModelInput(input) for input in inputs]
        if outputs is None:
            self.outputs = None
        else:
            self.outputs = [ModelOutput(out) for out in outputs]

    def get_type(self):
        return "SearchModelNode"

class Model(object):

    def __init__(self, mid, name=None, desc=None, model=None):
        self.id = mid
        self.name = name
        self.desc = desc
        self.model = model
    
    def add_description(self, model):
        self.model = model

    def get_default_output(self):
        """
        Just returns the first output

        """
        return self.model.outputs[0].name

    def __str__(self):
        out = json_format.MessageToJson(self.model)
        return out
        # return self.model

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
        
        out = Model(d.id, d)
        logger.debug("Got pipeline parsed: %s" % str(d))
        return out


    def to_file(self, fpath):
        """
        Writes the workflows to a file where the first line is tab separated
        list of solution ids. The second row contains a stringified version
        of the json for the corresponding solution id

        """
        return fpath

class SubModelNode(Model, ModelNode):

    def get_type(self):
        return "SubModelNode"

class ModelScores(object):

    def __init__(self, mdl, inputs, scores):
        # A ModeL id this score applies to
        self.mid = mdl.id
        # Inputs used to generate the score
        self.inputs = inputs
        # list of scores
        self.scores = scores

    def __dict__(self):
        out = {'model_id': self.mid,
               'inputs': self.inputs,
               # 'scores': [json_format.MessageToJson(score) for score in self.scores]
               'scores': self.scores
        }
        return out


    def __str__(self):
        out = {'model_id': self.mid,
               'inputs': self.inputs,
               'scores': [json_format.MessageToJson(score) for score in self.scores]
        }
        return json.dumps(out)


class Fit(object):

    def __init__(self, mdl, dataset, fit):
        self.mdl = mdl
        self.dataset = dataset
        self.fit = fit

