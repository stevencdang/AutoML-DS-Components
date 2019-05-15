
# Author: Steven C. Dang

# Class for selecting a dataset from a list of datasets

import logging
import os
import os.path as path
import sys
import json
import pprint
import argparse
import csv

from ls_dataset.d3m_dataset import D3MDataset

logger = logging.getLogger(__name__)

class DatasetSelector(object):
    """
    Select and import a dataset from a set of datasets

    """


    def run(self, ds_root, ds_name):
        """
        Main scripted oepration

        """
        ### Begin Script ###
        logger.info("Importing D3M Dataset selected by user")

        # Read in the dataset json
        datasets = {}
        names = set()
        for root, dirs, files in os.walk(ds_root):
            for f in files:
                if f == 'datasetDoc.json':
                    logger.debug("Found dataset in directory: %s" % root)
                    try: 
                        ds = D3MDataset.from_dataset_json(path.join(root, f))
                        if ds.name not in names:
                            logger.info("Found dataset name: %s\nAt path: %s" % (ds.name,  ds.dpath))
                            names.add(ds.name)
                            datasets[ds.name] = ds
                    except:
                        logger.warning("Error encountered whiel loading dataset json: %s" % path.join(root, f))


        ds = datasets[ds_name]

        logger.info("Found dataset with name %s, id: %s\n json: %s" % (ds.name, ds.id, str(ds)))

        return ds
