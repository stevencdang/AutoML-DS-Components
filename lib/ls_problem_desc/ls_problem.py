
# Author: Steven C. Dang

# Class representing a D3m problem description for pipeline search

import logging
import os.path as path
import os
from io import IOBase
import json
from datetime import datetime
import pprint

from ls_dataset.d3m_dataset import D3MDataset
from modeling.scores import Metric

logger = logging.getLogger(__name__)



class ProblemDesc(object):
    """
    Class representing a D3m problem description for pipeline search

    """
    
    def __init__(self, name=None, desc=None, task_type=None, subtype=None, version=1, metrics=None, metadata=None):
        """
        inputs: 
            metadata - dictionary representation of additional information
        
        """
        self.id = str(abs(hash(datetime.now())))
        self.name=name
        self.version=version
        self.description=desc
        self.task_type=task_type
        self.subtype = subtype
        if metrics is None:
            self.metrics=[]
        elif hasattr(metrics, '__iter__'):
            self.metrics = [Metric(m) for m in metrics]
        else:
            raise Exception("Invalid metrics given, must be a list")
        self.inputs = []
       
        # Catchall for extra information to support easy subclassing
        if metadata is not None:
            self.metadata = metadata
        else:
            self.metadata = None

    def add_input(self, did, res, col):
        if len(self.inputs) == 0:
            inpt = Input(did)
            inpt.add_target(res, col)
            self.inputs.append(inpt)
        else:
            added = False
            for inpt in self.inputs:
                if inpt.id == did:
                    inpt.add_target(res, col)
                    added = True

            if not added:
                inpt = Input(did)
                inpt.add_target(res,col)
                self.inputs.append(inpt)

    def to_dict(self):
        out = {
            "id": self.id,
            "version": self.version,
            "metrics": [metric.to_dict() for metric in self.metrics],
            "inputs": [inpt.to_dict() for inpt in self.inputs]
        }
        if self.name is not None:
            out["name"] = self.name
        if self.description is not None:
            out["description"] = self.description
        if self.task_type is not None:
            out["task_type"] = self.task_type
        if self.subtype is not None:
            out["task_subtype"] = self.subtype
        if self.metadata is not None:
            out["metadata"] = self.metadata
        return out

    def to_file(self, fpath):
        if isinstance(fpath, str):
            with open(fpath, 'w') as out_file:
                json.dump(self.to_dict(), out_file)
        elif isinstance(fpath, IOBase):
            json.dump(self.to_dict(), fpath)
        else:
            raise Exception("Invalid file/path given to write to file. Given \
                            input type: %s" % type(fpath))
    
    @staticmethod
    def from_json(fpath):
        """
        A static constructor of this class given a jsonified file

        """
        if isinstance(fpath, str):
            if path.exists(fpath):
                #Get dataset path from json path
                with open(fpath, 'r') as f:
                    ds_json = json.load(f)
            else:
                raise Exception("Found no problem schema json at path: %s" % str(fpath))
        elif isinstance(fpath, IOBase):
            logger.debug("Loading problem schema json from open file")
            ds_json = json.load(fpath)
        else:
            raise Exception("Found no problem schema json at path: %s" % str(fpath))

        logger.debug("Got raw problem schema json: %s" % str(ds_json))

        return ProblemDesc(
            name=ds_json['about']['problemName'], 
            desc=ds_json['about']['problemDescription'], 
            task_type=ds_json['about']['taskType'], 
            subtype=ds_json['about']['taskSubType'], 
            datasets=ds_json['inputs']['data'], 
            version=ds_json['about']['problemVersion'], 
            metrics=ds_json['inputs']['performanceMetrics'],
            metadata=ds_json
        )

    def __str__(self):
        return str(self.to_dict())

    def print(self):
        msg_json = self.to_dict()
        return pprint.pformat(msg_json)

       
    # def __str__(self):
        # return str(self.__iter__())

    # def __iter__(self):
        # d = {
            # 'datasetID': self.id,
            # 'targets': [str(t) for t in self.targets]
        # }
        # for k in d:
            # yield (k, d[k])


# class DSTarget(object):
    # def __init__(self, target_index, _id, col_index, col_name):
        # self.target_index = target_index
        # self.id = _id
        # self.col_index = col_index
        # self.col_name = col_name

    # def __str__(self):
        # return str(self.__iter__())

    # def __iter__(self):
        # d = {
            # 'targetIndex': self.target_index,
            # 'resID': str(self.id),
            # 'colIndex': self.col_index,
            # 'col_name': self.col_name
        # }
        # for k in d:
            # yield (k, d[k])


# class PerformanceMetric(object):
    # def __init__(self, metric):
        # self.metric = metric

    # def __iter__(self):
        # d =  {
            # 'metric': self.metric
        # }
        # for k in d:
            # yield (k, d[k])

    # def __str__(self):
        # out = {
            # 'metric': self.metric
        # }
        # return str(out)
        
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

class Input(object):
    def __init__(self, did):
        self.dataset_id = did
        self.targets = []

    def add_target(self, res, col):
        i = len(self.targets)
        target = Target(i, res, col)
        self.targets.append(target)

    def to_dict(self):
        out = {'dataset_id': self.dataset_id}
        out['targets'] = [t.to_dict() for t in self.targets]
        return out

    def __str__(self):
        return str(self.to_dict())

class Target(object):
    def __init__(self, indx, res=None, col=None):
        if col is not None:
            self.column_index = col.colIndex
            self.column_name = col.colName
        else:
            self.column_index = None
            self.column_name = None

        if res is not None:
            self.resource_id = res.resID
        else:
            self.resource_id = None

        self.target_index = indx

    def to_dict(self):
        return {
            'column_index': self.column_index,
            'column_name': self.column_name,
            'resource_id': self.resource_id,
            'target_index': self.target_index
        }


    def __str__(self):
        return str(self.to_dict())

