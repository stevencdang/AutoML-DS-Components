
# Author: Steven C. Dang

# Class representing a D3m problem description for pipeline search

import logging
import os.path as path
import os
from io import IOBase
import json
import pprint

from google.protobuf import json_format

# For testing as __main__
# from ls_problem import ProblemDesc
# from api_v3 import problem_pb2, problem_pb2_grpc

from .ls_problem import ProblemDesc
from .api_v3 import problem_pb2, problem_pb2_grpc

logger = logging.getLogger(__name__)

class D3MProblemDesc(ProblemDesc):

    __version__ = "D3M TA3TA2 API v2018.5.1"

    def __init__(self, prob, metadata=None):
        ds_json = json.loads(json_format.MessageToJson(prob))
        logger.debug(ds_json)
        ProblemDesc.__init__(
            self,
            name=prob.problem.name,
            desc=prob.problem.description,
            task_type=prob.problem.task_type,
            subtype=prob.problem.task_subtype,
            datasets=ds_json['inputs'],#prob.inputs, 
            version=prob.problem.version,
            metrics=ds_json['problem']['performanceMetrics'],#prob.problem.performance_metrics
            metadata=metadata
        )
        # Overide the autogenerated ID with the one given
        self.id = prob.problem.id
        self.d3m_prob = prob

    @staticmethod
    def from_string(msg):
        prob =  problem_pb2.ProblemDescription().ParseFromString(msg)
        return D3mProblemDesc(prob)

   
    @staticmethod
    def from_file(fpath):
        logger.info("Initializing D3MProblemDesc from json file")
        if isinstance(fpath, str):
            with open(fpath, 'r') as f:
                data = f.readlines()
        elif isinstance(fpath, IOBase):
            data = fpath.readlines()
        prob = json_format.Parse(data[0], problem_pb2.ProblemDescription())
        # with open(fpath, 'r') as f:
            # data = f.readlines()
        # prob = json_format.Parse(data, problem_pb2.ProblemDescription())
        logger.debug("Succesfully imported problem from json")
        return D3MProblemDesc(prob)

    @staticmethod
    def from_problem_desc(prob):
        logger.info("Initializing d3m problem doc from problem description class")
        pr = problem_pb2.Problem(
            id=prob.id,
            version=str(prob.version),
            name=prob.name,
            description=prob.description,
            task_type=D3MProblemDesc.get_task_type(prob.task_type)
        )
        if prob.subtype is not None:
            pr.task_subtype=D3MProblemDesc.get_task_subtype(prob.subtype)
        for metric in prob.metrics:
            m = pr.performance_metrics.add()
            m.metric = D3MProblemDesc.get_perf_metric(metric.metric)
            if 'k' in metric:
                m.k = metric['k']
            if 'pos_label' in metric:
                m.pos_label = metric['pos_label']

        pr_desc = problem_pb2.ProblemDescription(
            problem=pr
        )

        for dataset in prob.datasets:
            prob_input = pr_desc.inputs.add()
            prob_input.dataset_id = dataset.id
            for target in dataset.targets:
                t = prob_input.targets.add()
                if target.target_index == 0:
                    t.target_index = 1 # Override until I found out whnat this is used for
                else:
                    t.target_index = target.target_index
                t.resource_id = target.id
                t.column_index = target.col_index
                t.column_name = target.col_name

        return D3MProblemDesc(pr_desc, prob.metadata)

    @staticmethod
    def get_task_type(ttype):
        if isinstance(ttype, str):
            t = ttype.upper()
            if t == 'TASK_TYPE_UNDEFINED':
                return problem_pb2.TASK_TYPE_UNDEFINED
            elif t == 'CLASSIFICATION':
                return problem_pb2.CLASSIFICATION
            elif t == 'REGRESSION':
                return problem_pb2.REGRESSION
            elif t == 'CLUSTERING':
                return problem_pb2.CLUSTERING
            elif t == 'LINK_PREDICTION':
                return problem_pb2.LINK_PREDICTION
            elif t == 'VERTEX_NOMINATION':
                return problem_pb2.VERTEX_NOMINATION
            elif t == 'COMMUNITY_DETECTION':
                return problem_pb2.COMMUNITY_DETECTION
            elif t == 'GRAPH_CLUSTERING':
                return problem_pb2.GRAPH_CLUSTERING
            elif t == 'GRAPH_MATCHING':
                return problem_pb2.GRAPH_MATCHING
            elif t == 'TIME_SERIES_FORECASTING':
                return problem_pb2.TIME_SERIES_FORECASTING
            elif t == 'COLLABORATIVE_FILTERING':
                return problem_pb2.COLLABORATIVE_FILTERING
            else:
                return problem_pb2.TASK_TYPE_UNDEFINED
        else:
            t = ttype
            if t == problem_pb2.TASK_TYPE_UNDEFINED:
                return 'TASK_TYPE_UNDEFINED'
            elif t == problem_pb2.CLASSIFICATION:
                return 'CLASSIFICATION'
            elif t == problem_pb2.REGRESSION:
                return 'REGRESSION'
            elif t == problem_pb2.CLUSTERING:
                return 'CLUSTERING'
            elif t == problem_pb2.LINK_PREDICTION:
                return 'LINK_PREDICTION'
            elif t == problem_pb2.VERTEX_NOMINATION:
                return 'VERTEX_NOMINATION'
            elif t == problem_pb2.COMMUNITY_DETECTION:
                return 'COMMUNITY_DETECTION'
            elif t == problem_pb2.GRAPH_CLUSTERING:
                return 'GRAPH_CLUSTERING'
            elif t == problem_pb2.GRAPH_MATCHING:
                return 'GRAPH_MATCHING'
            elif t == problem_pb2.TIME_SERIES_FORECASTING:
                return 'TIME_SERIES_FORECASTING'
            elif t == problem_pb2.COLLABORATIVE_FILTERING:
                return 'COLLABORATIVE_FILTERING'
            else:
                return problem_pb2.TASK_TYPE_UNDEFINED

    @staticmethod
    def get_task_subtype(ttype):
        if isinstance(ttype, str):
            t = ttype.upper()
            if t == 'TASK_SUBTYPE_UNDEFINE':
                return problem_pb2.TASK_SUBTYPE_UNDEFINED
            elif t == 'NONE':
                return problem_pb2.NONE
            elif t == 'BINARY':
                return problem_pb2.BINARY
            elif t == 'MULTICLASS':
                return problem_pb2.MULTICLASS
            elif t == 'MULTILABEL':
                return problem_pb2.MULTILABEL
            elif t == 'UNIVARIATE':
                return problem_pb2.UNIVARIATE
            elif t == 'MULTIVARIATE':
                return problem_pb2.MULTIVARIATE
            elif t == 'OVERLAPPING':
                return problem_pb2.OVERLAPPING
            elif t == 'NONOVERLAPPING':
                return problem_pb2.NONOVERLAPPING
            else: 
                return problem_pb2.TASK_SUBTYPE_UNDEFINED
        else:
            t = ttype
            if t == problem_pb2.TASK_SUBTYPE_UNDEFINED:
                return 'TASK_SUBTYPE_UNDEFINED'
            elif t == problem_pb2.NONE:
                return 'NONE'
            elif t == problem_pb2.BINARY:
                return 'BINARY'
            elif t == problem_pb2.MULTICLASS:
                return 'MULTICLASS'
            elif t == problem_pb2.MULTILABEL:
                return 'MULTILABEL'
            elif t == problem_pb2.UNIVARIATE:
                return 'UNIVARIATE'
            elif t == problem_pb2.MULTIVARIATE:
                return 'MULTIVARIATE'
            elif t == problem_pb2.OVERLAPPING:
                return 'OVERLAPPING'
            elif t == problem_pb2.NONOVERLAPPING:
                return 'NONOVERLAPPING'
            else: 
                return 'TASK_SUBTYPE_UNDEFINED'


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
        msg_json = json.loads(self.__str__())
        if fpath is not None:
            logger.debug("Writing problem json to: %s" % fpath)
            with open(fpath, 'w') as out_file:
                json.dump(msg_json, out_file)

        return out

    def to_json_pretty(self, fpath=None):
        msg_json = json.loads(self.__str__())
        if fpath is not None:
            logger.debug("Writing readable problem json to: %s" % fpath)
            with open(fpath, 'w') as out_file:
                pprint.pprint(msg_json, out_file)

        return json.dumps(msg_json)


    def __str__(self):
        return json_format.MessageToJson(self.d3m_prob)

if __name__ == "__main__":
    logging.basicConfig()
    logger.info("Generating default problem doc")
    name = "Testing Problem Doc"
    desc = "A problem doc to test generating problem docs"
    task_type = "CLASSIFICATION"
    subtype = "NONE"
    version = 1
    metrics = [ {'metric': 'F1_MACRO'} ]
    datasets = [ {'dataset_id': '185_baseball_dataset', 'targets': [
        {
            'target_index': 0,
            'resource_id': "0",
            'column_index': 18,
            'column_name': 'Hall_of_Fame'
        }]
    }]
    prob_desc = ProblemDesc(name, desc, task_type, subtype, datasets=datasets, version=version, metrics=metrics)
    d3m_prob = D3MProblemDesc.from_problem_desc(prob_desc)
    print("Created D3m Problem Description: %s" % str(d3m_prob))
    
    
