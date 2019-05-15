
# Author: Steven C. Dang

# Class for scanning for available d3m datasets

import logging
import os.path as path
import os
import csv

from ls_dataset.d3m_dataset import D3MDataset

logger = logging.getLogger(__name__)

class DatasetImporter(object):
    """
    Scanning for available datasets

    """


    def run(self, ds_root):
        """
        Main scripted oepration

        """
        ### Begin Script ###
        logger.info("Importing List of available datasets")

        # Read in the dataset json
        datasets = set()
        for root, dirs, files in os.walk(ds_root):
            for f in files:
                if f == 'datasetDoc.json':
                    logger.debug("Found dataset in directory: %s" % root)
                    try:
                        ds = D3MDataset.from_dataset_json(path.join(root, f))
                        if ds.name not in datasets:
                            logger.info("Found dataset name: %s\nAt path: %s" % (ds.name,  ds.dpath))
                            datasets.add(ds.name)
                    except:
                        # Don't choke on unsupported dataset jsons
                        logger.warning("Encountered unsupported dataset: %s" % str(path.join(root, f)))

        logger.debug("Found datasets: %s" % str(datasets))

        return datasets




