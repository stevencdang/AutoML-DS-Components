
# Author: Steven C. Dang

# Class representing a D3m problem description for pipeline search

import logging
import os.path as path
import os
from io import IOBase
import json
import pprint
# from datetime import datetime

from google.protobuf import json_format

from .ls_problem import ProblemDesc, Input, Target
from .api_v3 import problem_pb2, problem_pb2_grpc
from modeling.scores import Metric

logger = logging.getLogger(__name__)

class GRPCProblemDesc(ProblemDesc):

    __version__ = "D3M TA3TA2 API v2018.5.1"

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

class DefaultProblemDesc(ProblemDesc):

    __default_schema__ = 'problemDoc.json'

    @staticmethod
    def from_file(fpath):
        logger.info("Initializing DefaultProblemDesc from json file")
        if isinstance(fpath, str):
            with open(fpath, 'r') as f:
                data = json.load(f)
        elif isinstance(fpath, IOBase):
            data = json.load(fpath)
        else:
            raise Exception("Expected path string or file io object to initialize \
                            Problem Description. Got %s instead" % type(fpath))
        # Initialize the class
        out = DefaultProblemDesc(
            name=data['about']['problemName'],
            version=data['about']['problemVersion'],
            desc = data['about']['problemDescription'],
            task_type = data['about']['taskType'],
            subtype = data['about']['taskSubType'],
            metrics = [metric['metric']
                       for metric in data['inputs']['performanceMetrics']],
            metadata = {
                            'schema_version': data['about']['problemSchemaVersion'],
                            'dataSplits': data['inputs']['dataSplits'],
                            'expectedOutputs': data['expectedOutputs'],
                            # 'original_json': data
                       }
        )
        # Overrite the auto-generated ID
        out.id = data['about']['problemID']
        # Manually create inputs and add them
        for d in data['inputs']['data']:
            inpt = Input(d['datasetID'])
            
            for t in d['targets']:
                target = Target(t['targetIndex'])
                target.resourceId = t['resID']
                target.columnIndex = t['colIndex']
                target.columnName = t['colName']
                inpt.targets.append(target)

            out.inputs.append(inpt)

        return out

    @staticmethod
    def from_problem_desc(prob):
        logger.info("Initializing Default problem desc from problem description class")
                              
        out = DefaultProblemDesc(
            name=prob.name,
            version=prob.version,
            desc = prob.description,
            task_type = prob.task_type,
            subtype = prob.subtype,
            metrics = prob.metrics,
            metadata = prob.metadata
        )
        out.inputs = prob.inputs
        return out

    def to_dict(self):
        out = {
            'about': {
                'problemID': self.id,
                'problemVersion': self.version
            },
            'inputs': {
                'data': [],
                'performanceMetrics': [],
            },
        }
        if self.name is not None:
            out['about']['problemName'] = self.name
        if self.description is not None:
            out['about']['problemDescription'] = self.description
        if self.task_type is not None:
            out['about']['taskType'] = self.task_type
        if self.subtype is not None:
            out['about']['taskSubType'] = self.subtype
        if len(self.metrics) > 0:
            out['inputs']['performanceMetrics'] = [m.to_dict() for m in self.metrics]
        if len(self.inputs) > 0:
            out['inputs']['data'] = [{
                'datasetID': inpt.dataset_id,
                'targets': [{
                    'targetIndex': t.target_index,
                    'resID': t.resource_id,
                    'colIndex': t.column_index,
                    'colName': t.column_name
                } for t in inpt.targets]
            } for inpt in self.inputs]
        
        if self.metadata is not None:
            if 'problemSchemaVersion' in self.metadata.keys():
                out['about']['problemSchemaVersion'] = self.metadata['problemSchemaVersion']
            if 'dataSplits' in self.metadata.keys():
                out['inputs']['dataSplits'] = self.metadata['dataSplits']
            if 'expectedOutputs' in self.metadata.keys():
                out['expectedOutputs'] = self.metadata['expectedOutputs']

        return out

    @staticmethod
    def get_default_problem(ds):
        """
        Return path to problem desc assuming default location given a dataset

        """
        dname = ds.name
        dpath = ds.dpath
        dir_name = path.split(dpath)[1]
        logger.debug("Getting problem for dataset with name, %s, and dataset_dir: %s" % (dname, dir_name))
        for root, dirs, files in os.walk(ds.dpath):
            for f in files:
                if f == DefaultProblemDesc.__default_schema__:
                    parent = path.split(root)[1]
                    if parent == dir_name + '_problem':
                        logger.debug("Getting problem schema at path: %s" % path.join(root, f))
                        return path.join(root, f)
        logger.warning("Found no default problem doc in dataset at: %s" % dpath)
        # return path.join(dpath, dname + '_problem', ProblemDesc.__default_schema__)
    
    def to_json(self, fpath=None):
        msg_json = self.to_dict()
        if fpath is not None:
            logger.debug("Writing problem json to: %s" % fpath)
            with open(fpath, 'w') as out_file:
                json.dump(msg_json, out_file)

        return msg_json

    def to_json_pretty(self, fpath=None):
        msg_json = self.to_dict()
        if fpath is not None:
            logger.debug("Writing readable problem json to: %s" % fpath)
            with open(fpath, 'w') as out_file:
                pprint.pprint(msg_json, out_file)

        return json.dumps(msg_json)


    def __str__(self):  
        out = self.to_dict()
        logger.debug("Problem to string: %s" % str(out))
        return str(out)

    
# class Problem(object):

    # def __init__(self, 
                 # pid=None, 
                 # name=None, 
                 # version=None,
                 # perf_metrics=None,
                 # task_type=None,
                 # task_subtype=None,
                 # desc=None):
        # self.id = pid
        # self.name = name
        # self.version = version
        # self.performanceMetrics = perf_metrics
        # self.taskType = task_type
        # self.taskSubtype = task_subtype
        # self.description = desc

    # @staticmethod
    # def from_protobuf(msg):
        # if 'id' in msg.keys():
            # id = msg.id
        # else:
            # id = None
        # if 'name' in msg.keys():
            # name = msg.name
        # else:
            # name = None
        # if 'version' in msg.keys():
            # version = msg.version
        # else:
            # version = None
        # if 'performanceMetrics' in msg.keys():
            # perf_metrics = msg.performanceMetrics
        # else:
            # perf_metrics = []
        # if 'taskType' in msg.keys():
            # task_type = msg.taskType
        # else:
            # task_type = None
        # if 'taskSubtype' in msg.keys():
            # task_subtype = msg.taskSubtype
        # else:
            # task_subtype = None
        # if 'description' in msg.keys():
            # desc = msg.description
        # else:
            # desc = None
        # return Problem( 
            # id=id,
            # name=name,
            # version=version,
            # performanceMetrics = perf_metrics,
            # taskType = task_type,
            # taskSubtype = task_subtype,
            # desc = desc
        # )

    # def __str__(self):
        # out = self.__dict__
        # out['performanceMetrics'] = [str(m) for m in self.performanceMetrics]
        # return str(out)

