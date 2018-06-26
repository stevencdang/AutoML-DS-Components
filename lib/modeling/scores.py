
# Author: Steven C. Dang

# Classes for scoring during modeling

import logging
import json
from google.protobuf import json_format


from d3m_ta2.api_v3 import problem_pb2

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

