
# Author: Steven C. Dang

# Class representing a D3m problem description for pipeline search

import logging
import os.path as path
import os
from io import IOBase
import json
import pprint
# from datetime import datetime

from google.protobuf.json_format import MessageToJson

from .ls_problem import *
from ls_dataset.d3m_dataset import DataAugmentationParameters
from ta3ta2_api import problem_pb2, problem_pb2_grpc
from modeling.scores import Metric

logger = logging.getLogger(__name__)

class GRPCProblemDesc(ProblemDesc):

    __version__ = "D3M TA3TA2 API v2018.5.1"

    def to_protobuf(self):
        prob = problem_pb2.Problem()
        if self.task_type is not None:
            prob.task_type = GRPCProblemDesc.get_task_type(self.task_type)
        if self.subtype is not None:
            prob.task_subtype = GRPCProblemDesc.get_task_subtype(self.subtype)
        for metric in self.metrics:
            m = prob.performance_metrics.add()
            m.metric = metric.get_perf_metric(metric.type)
            if metric.k is not None:
                m.k = metric.k
            if metric.pos is not None:
                m.pos_label = metric.pos
        msg = problem_pb2.ProblemDescription(
            id=self._id,
            problem=prob
        )
        msg.version = str(self.version)
        if self.name is not None:
            msg.name = self.name
        if self.description is not None:
            msg.description = self.description

        # logger.debug("Adding inputs: %s" % str(self.inputs))
        for inpt in self.inputs:
            i = msg.inputs.add()
            i.dataset_id = inpt.dataset_id
            for target in inpt.targets:
                t = i.targets.add()
                # logger.debug("adding target: %s" % str(target))
                t.target_index = target.target_index
                t.resource_id = target.resource_id
                t.column_index = target.column_index
                t.column_name = target.column_name
                if target.num_clusters is not None:
                    t.clusters_number = target.num_clusters
                # Clusters_number????
            for pfd in inpt.privileged_data:
                pd = i.privileged_data.add()
                pd.privileged_data_index = pfd.priviledged_data_index
                pd.resource_id = pfd.resource_id
                pd.column_index = pfd.col_index
                pd.column_name = pfd.col_name

        # Add data augmentation parameters
        for dap in self.data_aug_params:
            d = msg.data_augmentation.add()
            d.domain.extend(dap.domains)
            d.keywords.extend(dap.keywords)
            # for domain in dap.domains:
                # aug_domain = d.domain.add()
                # aug_domain = domain
            # for kw in dap.keywords:
                # aug_kw = d.keywords.add()
                # aug_kw = kw
        
        return msg

    def grpc_to_file(self, fpath):
        msg = self.to_protobuf()
        out_data = MessageToJson(msg) 
        if isinstance(fpath, str):
            with open(fpath, 'w') as out_file:
                out_file.write(out_data)
        elif isinstance(fpath, IOBase):
            fpath.write(out_data)
        else:
            raise Exception("Invalid file/path given to write to file. Given \
                            input type: %s" % type(fpath))

    
    @staticmethod
    def from_problem_desc(prob):
        logger.info("Initializing Default problem desc from problem description class")
        logger.debug("Problem description to translate to GRPC Prob Desc: %s" % str(prob.to_dict()))
                              
        out = GRPCProblemDesc(
            name=prob.name,
            version=prob.version,
            desc = prob.description,
            task_type = prob.task_type,
            subtype = prob.subtype,
            metrics = [m.type for m in prob.metrics],
            metadata = prob.metadata
        )
        out.inputs = prob.inputs
        out.data_aug_params = prob.data_aug_params
        logger.debug("GRPC Problem description: %s" % str(MessageToJson(out.to_protobuf())))
        return out

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
            elif t == 'VERTEX_CLASSIFICATION':
                return problem_pb2.VERTEX_CLASSIFICATION
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
            elif t == 'OBJECT_DETECTION':
                return problem_pb2.OBJECT_DETECTION
            elif t == 'SEMISUPERVISED_CLASSIFICATION':
                return problem_pb2.SEMISUPERVISED_CLASSIFICATION
            elif t == 'SEMISUPERVISED_REGRESSION':
                return problem_pb2.SEMISUPERVISED_REGRESSION
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
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        elif isinstance(fpath, IOBase):
            data = json.load(fpath)
        else:
            raise Exception("Expected path string or file io object to initialize \
                            Problem Description. Got %s instead" % type(fpath))
        # logger.debug("Read in Problem Doc from file: %s" % str(data))
        # Initialize the class
        if 'problemVersion' in data['about']:
            version = data['about']['problemVersion']
        else:
            version=None
        out = ProblemDesc(
            name=data['about']['problemName'],

            version=version,
            desc=data['about']['problemDescription'] if 'problemDescription' in data['about'].keys() else '',
            subtype = data['about']['taskSubType'] if 'taskSubType' in data['about'].keys() else '',
            metrics = [metric['metric']
                       for metric in data['inputs']['performanceMetrics']],
            metadata = {
                            # 'schema_version': data['about']['problemSchemaVersion'],
                            # 'dataSplits': data['inputs']['dataSplits'],
                            # 'expectedOutputs': data['expectedOutputs'],
                            # 'original_json': data
                       }
        )
        out.add_task_type(data['about']['taskType'])
        if 'problemSchemaVersion' in data['about'].keys():
            out.metadata['schema_version'] = data['about']['problemSchemaVersion']
        if 'dataSplits' in data['inputs'].keys():
            out.data_split = ProblemDataSplit()
            if 'method' in data['inputs']['dataSplits']:
                out.data_split.method = data['inputs']['dataSplits']['method']
            if 'testSize' in data['inputs']['dataSplits']:
                out.data_split.test_size = data['inputs']['dataSplits']['testSize']
            if 'numFolds' in data['inputs']['dataSplits']:
                out.data_split.num_folds = data['inputs']['dataSplits']['numFolds']
            if 'stratified' in data['inputs']['dataSplits']:
                out.data_split.stratified = data['inputs']['dataSplits']['stratified']
            if 'numRepeats' in data['inputs']['dataSplits']:
                out.data_split.num_repeats = data['inputs']['dataSplits']['numRepeats']
            if 'randomSeed' in data['inputs']['dataSplits']:
                out.data_split.random_seed = data['inputs']['dataSplits']['randomSeed']
            if 'splitsFile' in data['inputs']['dataSplits']:
                out.data_split.splits_file = data['inputs']['dataSplits']['splitsFile']
            if 'splitScript' in data['inputs']['dataSplits']:
                out.data_split.splitScript = data['inputs']['dataSplits']['splitScript']
        if 'expectedOutputs' in data.keys():
            out.expected_outputs = ExpectedProblemOutput()
            if 'predictionsFile' in data['expectedOutputs'].keys():
                out.expected_outputs.pred_file = data['expectedOutputs']['predictionsFile']
            if 'scoresFile' in data['expectedOutputs'].keys():
                out.expected_outputs.scores_file = data['expectedOutputs']['scoresFile']
        if 'dataAugmentation' in data.keys():
            out.data_aug_params = []
            for data_aug in data['dataAugmentation']:
                da = DataAugmentationParameters()
                if 'domain' in data_aug:
                    da.domains = data_aug['domain']
                if 'keywords' in data_aug:
                    da.keywords = data_aug['keywords']
                out.data_aug_params.append(da)
            

        # Overrite the auto-generated ID
        # out.id = data['about']['problemID']

        # Manually create inputs and add them
        for d in data['inputs']['data']:
            inpt = Input(d['datasetID'])
            
            for t in d['targets']:
                target = Target(t['targetIndex'])
                target.resource_id = t['resID']
                target.column_index = t['colIndex']
                target.column_name = t['colName']
                if 'numClusters' in t:
                    target.num_clusters = t['numClusters']
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
        out.id = prob['id']
        out.inputs = prob.inputs
        return out
    
    def to_file(self, fpath):
        if isinstance(fpath, str):
            with open(fpath, 'w') as out_file:
                json.dump(super().to_dict(), out_file)
        elif isinstance(fpath, IOBase):
            json.dump(super().to_dict(), fpath)
        else:
            raise Exception("Invalid file/path given to write to file. Given \
                            input type: %s" % type(fpath))


    def print(self, fpath=None):
        msg_json = super().to_dict()
        if fpath is None:
            return pprint.pformat(msg_json)
        else:
            logger.debug("Writing readable problem json to: %s" % fpath)
            with open(fpath, 'w') as out_file:
                pprint.pprint(msg_json, out_file)
            return pprint.pformat(msg_json)


    def to_dict(self):
        logger.debug("######################################")
        logger.debug("DefaultProblmDesc to dict")
        logger.debug("######################################")
        out = {
            'about': {
                'problemID': self._id,
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
        logger.debug("Getting problem from dataset: %s" % str(ds))
        dname = ds.name
        dpath = path.dirname(ds.dpath)
        logger.debug("Looking for problem in dataset path: %s" % dpath)
        ds_dir_name = path.split(ds.dpath)[1]
        if ds_dir_name.endswith('_dataset'):
            dir_name = ds_dir_name[:-8]
        else:
            dir_name = ds_dir_name
        logger.debug("Getting problem for dataset with name, %s, and dataset_dir: %s" % (dname, dir_name))
        # for root, dirs, files in os.walk(ds.dpath):
        result = None
        for root, dirs, files in os.walk(dpath):
            for f in files:
                if f == DefaultProblemDesc.__default_schema__:
                    parent = path.split(root)[1]
                    result = path.join(root, f)
                    logger.debug("Found problem doc at path: %s" % result)
                    if parent == dir_name + '_problem':
                        logger.debug("Getting problem schema at path: %s" % result)
                        return result
        if result is not None: 
            logger.warning("Getting problem schema at unexpected path: %s" % result)
            return result
        else:
            logger.warning("Found no default problem doc in dataset at: %s" % dpath)
    
    def __str__(self):  
        out = self.to_dict()
        logger.debug("Problem to string: %s" % str(out))
        return str(out)

