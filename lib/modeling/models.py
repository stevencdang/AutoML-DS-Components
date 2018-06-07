
# Author: Steven C. Dang

# Class representing an ordered set of operations on a given data input

import logging
import json
from abc import ABC, abstractmethod

from google.protobuf import json_format
from protobuf_to_dict import protobuf_to_dict

from d3m_ta2.api_v3 import core_pb2, pipeline_pb2, problem_pb2, value_pb2

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

    def __init__(self, my_type, k=None, pos=None ):
        logger.debug("Initializing Metric with type: %s" % my_type)
        self.type = self.get_match(my_type)
        self.k = k
        self.pos = pos

    def __eq__(self, other):
        return self.type == other.type

    def __ne__(self, other):
        return self.type != other.type

    def is_match(self, t):
        return self.get_match(t) == self.type

    def __str__(self):
        return self.type

    @staticmethod
    def from_json(d):
        logger.debug("Loading metric from json given type: %s\t and data: %s" % (type(d), str(d)))
        if isinstance(d, str):
            d = json.loads(d)
        if 'k' in d.keys():
            k = d['k']
        else:
            k = None
        if 'pos_label' in d.keys():
            pos = d['pos_label']
        else:
            pos = None
        return Metric(d['metric'], k, pos)

    def __dict__(self):
        return {'metric': self.type}

    def __str__(self):
        return str(self.__dict__())

    def to_protobuf(self):
        msg = problem_pb2.ProblemPerformanceMetric(
            metric = self.get_perf_metric(self.type),
            k = self.k,
            pos_label = self.pos
        )
        return msg

    @staticmethod
    def from_protobuf(msg):
        data = json_format.MessageToJson(msg)#, problem_pb2.ProblemPerformanceMetric)
        return Metric.from_json(data)

    
    @staticmethod
    def get_types():
        types = []
        for m in Metric.__types__:
            t = m.lower()
            for char in Metric.__ignore_chars__:
                t.replace(char, "")
            types.append(t)
        return types

    @staticmethod
    def get_match(t):
        if type(t) is int:
            logger.debug("Converting to enum name: %i" % t)
            t = problem_pb2.PerformanceMetric.Name(t)
            logger.debug("Got enum name: %s" % t)
        t = Metric.convert_type(t)
        try:
            i = Metric.get_types().index(t)
            return Metric.__types__[i]
        except ValueError:
            return None

    @staticmethod
    def convert_type(t):
        t = t.lower()
        for char in Metric.__ignore_chars__:
            t.replace(char, "")
        return t

    @staticmethod
    def is_valid(t):
        return Metric.convert_types(t) in Metric.get_types()

    @staticmethod
    def get_perf_metric(metric):
        if isinstance(metric, str):
            m = metric.upper()
            if m == 'METRIC_UNDEFINED':
                return problem_pb2.METRIC_UNDEFINED
            elif m == 'ACCURACY':
                return problem_pb2.ACCURACY
            elif m == 'F1':
                return problem_pb2.F1
            elif m == 'F1_MICRO' or m.lower() == 'f1macro':
                return problem_pb2.F1_MICRO
            elif m == 'F1_MACRO':
                return problem_pb2.F1_MACRO
            elif m == 'ROC_AUC':
                return problem_pb2.ROC_AUC
            elif m == 'ROC_AUC_MICRO':
                return problem_pb2.ROC_AUC_MICRO
            elif m == 'ROC_AUC_MACRO':
                return problem_pb2.ROC_AUC_MACRO
            elif m == 'MEAN_SQUARED_ERROR':
                return problem_pb2.MEAN_SQUARED_ERROR
            elif m == 'ROOT_MEAN_SQUARED_ERROR':
                return problem_pb2.ROOT_MEAN_SQUARED_ERROR
            elif m == 'ROOT_MEAN_SQUARED_ERROR_AVG':
                return problem_pb2.ROOT_MEAN_SQUARED_ERROR_AVG
            elif m == 'MEAN_ABSOLUTE_ERROR':
                return problem_pb2.MEAN_ABSOLUTE_ERROR
            elif m == 'R_SQUARED':
                return problem_pb2.R_SQUARED
            elif m == 'NORMALIZED_MUTUAL_INFORMATION':
                return problem_pb2.NORMALIZED_MUTUAL_INFORMATION
            elif m == 'JACCARD_SIMILARITY_SCORE':
                return problem_pb2.JACCARD_SIMILARITY_SCORE
            elif m == 'PRECISION_AT_TOP_K':
                return problem_pb2.PRECISION_AT_TOP_K
            elif m == 'LOSS':
                return problem_pb2.LOSS
            else:
                raise Exception ("Invalid metric given: %s" % m)
        else:
            m = metric
            if m == problem_pb2.METRIC_UNDEFINED:
                return 'METRIC_UNDEFINED'
            elif m == problem_pb2.ACCURACY:
                return 'ACCURACY'
            elif m == problem_pb2.F1:
                return 'F1'
            elif m == problem_pb2.F1_MICRO:
                return 'F1_MICRO'
            elif m == problem_pb2.F1_MACRO:
                return 'F1_MACRO'
            elif m == problem_pb2.ROC_AUC:
                return 'ROC_AUC'
            elif m == problem_pb2.ROC_AUC_MICRO:
                return 'ROC_AUC_MICRO'
            elif m == problem_pb2.ROC_AUC_MACRO:
                return 'ROC_AUC_MACRO'
            elif m == problem_pb2.MEAN_SQUARED_ERROR:
                return 'MEAN_SQUARED_ERROR'
            elif m == problem_pb2.ROOT_MEAN_SQUARED_ERROR:
                return 'ROOT_MEAN_SQUARED_ERROR'
            elif m == problem_pb2.ROOT_MEAN_SQUARED_ERROR_AVG:
                return 'ROOT_MEAN_SQUARED_ERROR_AVG'
            elif m == problem_pb2.MEAN_ABSOLUTE_ERROR:
                return 'MEAN_ABSOLUTE_ERROR'
            elif m == problem_pb2.R_SQUARED:
                return 'R_SQUARED'
            elif m == problem_pb2.NORMALIZED_MUTUAL_INFORMATION:
                return 'NORMALIZED_MUTUAL_INFORMATION'
            elif m == problem_pb2.JACCARD_SIMILARITY_SCORE:
                return 'JACCARD_SIMILARITY_SCORE'
            elif m == problem_pb2.PRECISION_AT_TOP_K:
                return 'PRECISION_AT_TOP_K'
            elif m == problem_pb2.LOSS:
                return 'LOSS'
            else:
                raise Exception ("Invalid metric given: %s" % str(m))

    def to_json(self, fpath=None):
        out = self.__str__()

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
        
        out = Model(d.id, model=d)
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

    def __init__(self, mid, inputs, scores):
        # A ModeL id this score applies to
        self.mid = mid
        # Inputs used to generate the score
        self.inputs = inputs
        # list of scores
        self.scores = scores

    def __dict__(self):
        out = {'model_id': self.mid,
               'inputs': self.inputs,
               # 'scores': [json_format.MessageToJson(score) for score in self.scores]
               # 'scores': [protobuf_to_dict(score) for score in self.scores]
               'scores': [score.__dict__() for score in self.scores]
        }
        return out

    def __str__(self):
        out = self.__dict__()
        logger.debug("########################")
        logger.debug("########################")
        logger.debug("########################")
        logger.debug(len(self.scores))
        logger.debug(self.scores)
        logger.debug("########################")
        logger.debug([str(score) for score in self.scores])
        # logger.debug("########################")
        logger.debug(json.dumps(out))
        logger.debug("########################")
        logger.debug("########################")
        logger.debug("########################")
        return json.dumps(out)
    
    @staticmethod
    def from_json(raw_data):
        logger.debug("########################")
        logger.debug("Got raw data:\n%s" % raw_data)
        data = json.loads(raw_data)
        logger.debug("########################")
        logger.debug("data keys: %s" % data.keys())
        logger.debug("########################")
        logger.debug("Model id: %s" % data['model_id'])
        logger.debug("########################")
        logger.debug("Model inputs: %s" % data['inputs'])
        logger.debug("########################")
        logger.debug("Model scores: %s" % [str(score) for score in data['scores']])
        logger.debug("Model scores: %s" % [Score.from_json(score) for score in data['scores']])
        return ModelScores(data['model_id'], data['inputs'],[Score.from_json(score) for score in data['scores']])

class Score(object):

    def __init__(self, metric, fold, targets, value):
        self.metric = metric
        self.fold = fold
        if targets is None:
            self.targets = []
        else:
            self.targets = targets
        self.value = value

    @staticmethod
    def from_json(data):
        if isinstance(data, str):
            data = json.loads(data)
        metric = Metric.from_json(data['metric'])        
        val = Value.from_json(data['value'])
        if 'targets' in data:
            targets = data['targets']
        else:
            targets = []
        return Score(metric, data['fold'], targets, val)

    @staticmethod
    def from_protobuf(msg):
        metric = Metric.from_protobuf(msg.metric)
        targets = [json_format.MessageToJson(target) for target in msg.targets]
        val = Value.from_protobuf(msg.value)
        return Score(metric, msg.fold, targets, val)

    def to_protobuf(self):
        msg = core_pb2.Score(
            fold=self.fold,
            metric=self.metric.to_protobuf(),
            value=self.value.to_protobuf()
        )
        # msg.metric = self.metric.to_protobuf()
        if len(self.targets) > 0:
            msg.targets = targets
        # msg.value = self.value.to_protobuf()
        return msg

    def __dict__(self):
        return {
            'metric': self.metric.__dict__(),
            'fold': self.fold,
            'targets': self.targets,
            'value': self.value.__dict__(),
        }

    def __str__(self):
        return json_format.MessageToJson(self.to_protobuf())

class Value(object):

    def __init__(self, val, vtype):
        self.value = val
        self.type = vtype

    @staticmethod
    def from_json(msg):
        logger.debug("Creating Value from %s: %s" % (str(type(msg)), str(msg)))
        mtype = list(msg.keys())[0]
        val = msg[mtype]
        return Value(val, mtype)

    @staticmethod
    def from_protobuf(msg):
        d = json.loads(json_format.MessageToJson(msg))
        logger.debug("Got msg json: %s" % str(d))
        return Value.from_json(d)

    def to_protobuf(self):
        msg = value_pb2.Value(
        )
        setattr(msg, self.type, self.value)
        return msg

    def __dict__(self):
        return {
            self.type: self.value
        }
    def __str__(self):
        return str({str(self.type): self.value})

        

class Fit(object):

    def __init__(self, mdl, dataset, fit):
        self.mdl = mdl
        self.dataset = dataset
        self.fit = fit

