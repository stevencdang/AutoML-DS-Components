
# Author: Steven C. Dang

# Classes for scoring during modeling

import logging
import json
from json import JSONDecodeError
import ast
from google.protobuf import json_format

from ta3ta2_api import problem_pb2

from .models import Model, DBModel

logger = logging.getLogger(__name__)

class Metric(object):

    __types__ = [
        "accuracy",
        "precision",
        "recall",
        "f1",
        "f1Micro",
        "f1Macro",
        "rocAuc",
        "rocAucMacro",
        "rocAucMicro",
        "meanSquaredError",
        "rootMeanSquaredError",
        "meanAbsoluteError",
        "rSquared",
        "normalizedMutualInformation",
        "jaccardSimilarityScore",
        "precisionAtTopK",
        "objectDetectionAP",
        "hammingLoss",
        "averageMeanReciprocalRank"
    ]

    __ignore_chars__ = ['-', '_']

    def __init__(self, my_type, k=None, pos=None ):
        """
        my_type is either a string or an int that correlates with an enum of
        all available types

        """
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
        logger.debug("Initializing Metric with type: %s\tvalue: %s" % (type(d['metric']), str(d['metric'])))
        return Metric(d['metric'], k, pos)

    def to_dict(self):
        out = {'metric': self.type}
        if self.k is not None:
            out['k'] = self.k
        if self.pos is not None:
            out['pos_label'] = self.pos
        return out


    def __str__(self):
        return str(self.to_dict())

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
        return [Metric.convert_type(m) for m in Metric.__types__]

    @staticmethod
    def get_match(t):
        if type(t) is int:
            # logger.debug("Converting to enum name: %i" % t)
            t = problem_pb2.PerformanceMetric.Name(t)
            # logger.debug("Got enum name: %s" % t)
        convert_t = Metric.convert_type(t)
        # logger.debug("Got match of %s with %s" % (t, convert_t))
        # logger.debug("Looking for match in types: %s" % str(Metric.get_types()))
        try:
            i = Metric.get_types().index(convert_t)
            return Metric.__types__[i]
        except ValueError:
            return None

    @staticmethod
    def convert_type(t):
        t = t.lower()
        for char in Metric.__ignore_chars__:
            t = t.replace(char, "")
        return t

    @staticmethod
    def is_valid(t):
        return Metric.convert_types(t) in Metric.get_types()

    @staticmethod
    def get_perf_metric(metric):
        if isinstance(metric, str):
            m = Metric.convert_type(metric)
            if m == 'metricundefined':
                return problem_pb2.METRIC_UNDEFINED
            elif m == 'accuracy':
                return problem_pb2.ACCURACY
            elif m == 'precision':
                return problem_pb2.PRECISION
            elif m == 'recall':
                return problem_pb2.RECALL
            elif m == 'f1':
                return problem_pb2.F1
            elif m == 'f1micro':
                return problem_pb2.F1_MICRO
            elif m == 'f1macro':
                return problem_pb2.F1_MACRO
            elif m == 'rocauc':
                return problem_pb2.ROC_AUC
            elif m == 'rocaucmicro':
                return problem_pb2.ROC_AUC_MICRO
            elif m == 'rocaucmacro':
                return problem_pb2.ROC_AUC_MACRO
            elif m == 'meansquarederror':
                return problem_pb2.MEAN_SQUARED_ERROR
            elif m == 'rootmeansquarederror':
                return problem_pb2.ROOT_MEAN_SQUARED_ERROR
            # elif m == 'rootmeansquarederroravg':
                # return problem_pb2.ROOT_MEAN_SQUARED_ERROR_AVG
            elif m == 'meanabsoluteerror':
                return problem_pb2.MEAN_ABSOLUTE_ERROR
            elif m == 'rsquared':
                return problem_pb2.R_SQUARED
            elif m == 'normalizedmutualinformation':
                return problem_pb2.NORMALIZED_MUTUAL_INFORMATION
            elif m == 'jaccardsimilarityscore':
                return problem_pb2.JACCARD_SIMILARITY_SCORE
            elif m == 'precisionattopk':
                return problem_pb2.PRECISION_AT_TOP_K
            elif m == 'objectdetectionap':
                return problem_pb2.OBJECT_DETECTION_AVERAGE_PRECISION
            elif m == 'hammingloss':
                return problem_pb2.HAMMING_LOSS
            elif m == 'averagemeanreciprocalrank':
                return problem_pb2.RANK
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
            # elif m == problem_pb2.ROOT_MEAN_SQUARED_ERROR_AVG:
                # return 'ROOT_MEAN_SQUARED_ERROR_AVG'
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
            elif m == problem_pb2.OBJECT_DETECTION_AVERAGE_PRECISION:
                return 'OBJECT_DETECTIONAP'
            elif m == problem_pb2.HAMMING_LOSS:
                return 'HAMMING_LOSS'
            elif m == problem_pb2.RANK:
                return 'AVERAGE_MEAN_RECIPROCAL_RANK'
            else:
                raise Exception ("Invalid metric given: %s" % str(m))
    
    @staticmethod
    def get_valid_metrics(dtype):
        dtype = dtype.lower()
        if dtype == 'integer':
            return []
        elif dtype == 'real':
            return []
        elif dtype =='categorical':
            return []
        elif dtype == 'string':
            return []
        elif dtype == 'boolean':
            return []
        else:
            logger.warning("Unrecognized type. Defaulting to all supported metrics")
            return Metric.__types__


    def to_json(self, fpath=None):
        out = self.__str__()

    @staticmethod
    def get_metric_order(metric):
        m = Metric.convert_type(metric)
        if m in [
                "accuracy",
                "precision",
                "recall",
                "f1",
                "f1Micro",
                "f1Macro",
                "rocAuc",
                "rocAucMacro",
                "rocAucMicro",
                "rSquared",
                "normalizedMutualInformation",
                "jaccardSimilarityScore",
                "precisionAtTopK",
                "objectDetectionAP",
                "averageMeanReciprocalRank"
        ]:
            return "higher_is_better"
        elif m in [
                "meanSquaredError",
                "rootMeanSquaredError",
                "meanAbsoluteError",
                "hammingLoss"
        ]:
            return "lower_is_better"
        else:
            logger.warning("Uncertain order of given metric, %s, returning Higher is Better" %
                           m)
            return "higher_is_better"


class ModelScores(DBModel):

    def __init__(self, mid, inputs, scores, _id=None):
        logger.debug("ModelScore initialized with id: %s\ninputs: %s\nscores: %s" % (mid, str(inputs), str(scores)))
        # A ModeL id this score applies to
        self.mid = mid
        # Inputs used to generate the score
        self.inputs = inputs
        # list of scores
        self.scores = scores
        super().__init__(_id)

    def to_dict(self):
        # out = self.__dict__
        out = {'_id': self._id,
               'mid': self.mid,
               'inputs': self.inputs,
               'scores': [score.to_dict() for score in self.scores]
        }
        # out['scores'] = [score.to_dict() for score in self.scores]
        return out

    def to_json(self):
        # Override DBModel version of to_json
        return self.to_dict()

    def __str__(self):
        out = self.to_dict()
        return json.dumps(out)
    
    @staticmethod
    def from_json(inpt):
        if isinstance(inpt, str):
            try: 
                data = json.loads(inpt)
            except JSONDecodeError:
                data = ast.literal_eval(inpt)
        elif isinstance(inpt, dict):
            data = inpt
        logger.debug("Loading from json: %s" % str(data))
        return ModelScores(data['model_id'], data['inputs'],[Score.from_json(score) for score in data['scores']])

class Score(object):

    def __init__(self, metric, fold, value):
        self.metric = metric
        self.fold = fold
        self.value = value

    @staticmethod
    def from_json(inpt):
        if isinstance(inpt, str):
            try: 
                data = json.loads(inpt)
            except JSONDecodeError:
                data = ast.literal_eval(inpt)
        elif isinstance(inpt, dict):
            data = inpt

        metric = Metric.from_json(data['metric'])        
        val = Value.from_json(data['value'])
        return Score(metric, data['fold'], val)

    @staticmethod
    def from_protobuf(msg):
        metric = Metric.from_protobuf(msg.metric)
        val = Value.from_protobuf(msg.value)
        return Score(metric, msg.fold, val)

    def to_protobuf(self):
        msg = core_pb2.Score(
            fold=self.fold,
            metric=self.metric.to_protobuf(),
            value=self.value.to_protobuf()
        )
        return msg

    def to_dict(self):
        return {
            'metric': self.metric.to_dict(),
            'fold': self.fold,
            'value': self.value.to_dict(),
        }

    def __str__(self):
        return str(self.to_dict())

class Value(object):

    def __init__(self, val, vtype):
        self.value = val
        self.type = vtype

    @staticmethod
    def from_json(inpt):
        if isinstance(inpt, str):
            try: 
                data = json.loads(inpt)
            except JSONDecodeError:
                data = ast.literal_eval(inpt)
        elif isinstance(inpt, dict):
            data = inpt

        logger.debug("Creating Value from %s: %s" % (str(type(data)), str(data)))
        mtype = list(data.keys())[0]
        val = data[mtype]
        return Value(val, mtype)

    @staticmethod
    def from_protobuf(msg):
        d = json.loads(json_format.MessageToJson(msg))
        logger.debug("Got msg json: %s" % str(d))
        return Value.from_json(d)

    def to_protobuf(self):
        msg = value_pb2.Value()
        setattr(msg, self.type, self.value)
        return msg

    def to_dict(self):
        return {
            self.type: self.value
        }

    def __str__(self):
        return str(self.to_dict())

        

class Fit(object):

    def __init__(self, mdl, dataset, fit):
        self.mdl = mdl
        self.dataset = dataset
        self.fit = fit

class RankedModel(DBModel):

    def __init__(self, mdl, rank, _id=None):
        self.mdl = mdl
        self.rank = rank
        super().__init__(_id)

    def update_rank(self, rank):
        self.rank = rank

    def to_dict(self):
        return {
            '_id': self._id,
            'model': self.mdl.to_dict(),
            'rank': self.rank
        }

    def to_json(self):
        return self.to_dict()

    def __str__(self):
        return str(self.to_dict())

    @staticmethod
    def from_json(inpt):
        if isinstance(inpt, str):
            try: 
                data = json.loads(inpt)
            except JSONDecodeError:
                data = ast.literal_eval(inpt)
        elif isinstance(inpt, dict):
            data = inpt

        logger.debug("Creating RankedModel from %s: %s" % (str(type(data)), str(data)))
        model = Model.from_json(data['model'])
        return RankedModel(mdl=model, rank=data['rank'], _id=data['_id'])
