
# Author: Steven C. Dang

# Class representing a D3m problem description for pipeline search

import logging
import os.path as path
import os
from io import IOBase
import json
import hashlib
from datetime import datetime
import pprint

from ls_dataset.d3m_dataset import D3MDataset

logger = logging.getLogger(__name__)



class ProblemDesc(object):
    """
    Class representing a D3m problem description for pipeline search

    """

    __default_schema__ = 'problemDoc.json'
    
    def __init__(self, name, desc, task_type, subtype, datasets=None, version=1, metrics=None, metadata=None):
        """
        inputs: 
            metadata - dictionary representation of the problem schema
        
        """
        h = hashlib.sha1()
        h.update(str(datetime.now()).encode('utf-8'))
        self.id = h.hexdigest()
        self.version=version
        self.name=name
        self.description=desc
        self.task_type=task_type

        if subtype is not None:
            self.subtype = subtype
        else:
            self.subtype = None

        if metrics is None:
            self.metrics=[]
        elif hasattr(metrics, '__iter__'):
            self.metrics = [PerformanceMetric(m['metric']) for m in metrics]
        else:
            self.metrics = [PerformanceMetric(metrics['metric'])]
        try:
            if datasets is None:
                self.datasets = []
            elif hasattr(datasets, '__iter__'):
                self.datasets = [Dataset(d['datasetID'], d['targets']) for d in datasets]
            else:
                self.datasets = [Dataset(d['datasetID'], d['targets'])]
        except KeyError:
            if datasets is None:
                self.datasets = []
            elif hasattr(datasets, '__iter__'):
                self.datasets = [Dataset(d['datasetId'], d['targets']) for d in datasets]
            else:
                self.datasets = [Dataset(d['datasetId'], d['targets'])]
        
        if metadata is not None:
            self.metadata = metadata
            self.about = metadata['about']
            self.inputs = metadata['inputs']
            self.expectedOutputs = metadata['expectedOutputs']
        else:
            self.about = None
            self.inputs = None
            self.expectedOutputs = None
            self.metadata = None


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
                if f == ProblemDesc.__default_schema__:
                    parent = path.split(root)[1]
                    if parent == dir_name + '_problem':
                        logger.debug("Getting problem schema at path: %s" % path.join(root, f))
                        return path.join(root, f)
        logger.warning("Found no default problem doc in dataset at: %s" % dpath)
        # return path.join(dpath, dname + '_problem', ProblemDesc.__default_schema__)
    
    
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
        
    
    def to_json(self, fpath=None):
        """
        Write the problem description to file and return a string with the json. 
        If no path is given, then just returns a string with the json 
        representation of the problem description

        """
        out = self.__iter__()
        logger.debug("Writing to json: %s" % out)

        if fpath is not None:
            logger.debug("Writing dataset json to: %s" % fpath)
            out_file = open(fpath, 'w')
            json.dump(out, out_file)
            out_file.close()

        return out

    def to_json_pretty(self, fpath=None):
        out = self.print()
        logger.debug("Writing to pretty json: %s" % out)
        if fpath is not None:
            logger.debug("Writing problem json in human readable format to: %s" % fpath)
            with open(fpath, 'w') as out_file:
                out_file.write(out)

        return out

    def print(self):
        # out = self.__str__()
        # ds_json = json.loads(out)
        ds_json = self.__iter__()
        return pprint.pformat(ds_json)

    def __iter__(self):
        out = {
            'about': {
                'problemID': self.id,
                'problemName': self.name,
                'problemDescription': self.description,
                'taskType': self.task_type,
                'taskSubType': self.subtype,
                'problemVersion': self.version,
            },
            'inputs': {
                'data': [],
                'performanceMetrics': []
            },
            'expectedOutputs': {
                'predictionsFile': "predictions.csv"
            }
        }
        if self.metadata is not None:
            out['inputs'] = self.inputs
            out['expectedOutputs'] =  self.expectedOutputs
            out['about']['problemSchemaVersion'] = self.about['problemSchemaVersion']
        else:
            for metric in self.metrics:
                out['inputs']['performanceMetrics'].append(
                    metric.__iter__()
                )
                    # {
                    # 'metric': metric
                # })
            for ds in self.datasets:
                out['inputs']['data'].append(
                    # ds.__iter__()
                    { k: ds[k] for k in ds }
                )
                    # 'datasetID': ds.id,
                    # 'targets': {
                        # 'targetIndex': ds['target_index'],
                        # 'resID': str(ds['res_id']),
                        # 'colIndex': ds['col_index'],
                        # 'colName': ds['col_name']
                    # }

                # })

        return out



    def __str__(self):
        return json.dumps(self.__iter__())


class Dataset(object):
    def __init__(self, _id, targets):
        self.id = _id
        # logger.debug(targets)
        try:
            self.targets = [DSTarget(t['targetIndex'], t['resID'], t['colIndex'], t['colName']) for t in targets]
        except KeyError:
            self.targets = [DSTarget(t['targetIndex'], t['resourceId'], t['columnIndex'], t['columnName']) for t in targets]


    def __str__(self):
        return str(self.__iter__())

    def __iter__(self):
        d = {
            'datasetID': self.id,
            'targets': [str(t) for t in self.targets]
        }
        for k in d:
            yield (k, d[k])


class DSTarget(object):
    def __init__(self, target_index, _id, col_index, col_name):
        self.target_index = target_index
        self.id = _id
        self.col_index = col_index
        self.col_name = col_name

    def __str__(self):
        return str(self.__iter__())

    def __iter__(self):
        d = {
            'targetIndex': self.target_index,
            'resID': str(self.id),
            'colIndex': self.col_index,
            'col_name': self.col_name
        }
        for k in d:
            yield (k, d[k])


class PerformanceMetric(object):
    def __init__(self, metric):
        self.metric = metric

    def __iter__(self):
        d =  {
            'metric': self.metric
        }
        for k in d:
            yield (k, d[k])

    def __str__(self):
        out = {
            'metric': self.metric
        }
        return str(out)
        
        


if __name__ == "__main__":
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
            'columns_name': 'Hall_of_Fame'
        }]
    }]

    ProblemDesc(name, desc, task_type, subtype, datasets=dataset, version=version, metrics=metrics)
    
