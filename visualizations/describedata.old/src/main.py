
# Author: Steven C. Dang

# Main script for generating a confusion matrix viz taking in a d3m dataset and a prediction


import logging
import sys
from os import path
import os
import argparse
import itertools
from shutil import copytree, rmtree, copyfile
# import requests

import pandas as pd
# import numpy as np
# import matplotlib
# matplotlib.use("agg")
# import matplotlib.pyplot as plt
# from sklearn.metrics import confusion_matrix

from jinja2 import Environment, PackageLoader, select_autoescape

# Workflow component specific imports
from ls_utilities.ls_logging import setup_logging
from ls_utilities.cmd_parser import get_default_arg_parser
from ls_utilities.ls_wf_settings import *

from ls_dataset.d3m_dataset import D3MDataset

__version__ = '0.1'


class LS_Path_Factory(object):

    def __init__(self, workingDir, programDir):
        self.workingDir = workingDir
        self.programDir = programDir

    def get_out_path(self, fpath):
        return path.join(self.workingDir, fpath)

    def get_hosted_path(self, fpath):
        return "LearnSphere?htmlPath=" + self.get_out_path(fpath)


if __name__ == '__main__':
    # Parse argumennts
    parser = get_default_arg_parser("Visualize Describe Data")
    parser.add_argument('-file0', type=argparse.FileType('r'),
                       help='the dataset json including pipeline search result')
    args = parser.parse_args()

    if args.is_test is not None:
        is_test = args.is_test == 1
    else:
        is_test = False

    # Get config file
    config = SettingsFactory.get_settings(path.join(args.programDir, 'program', 'settings.cfg'), 
                                          program_dir=args.programDir,
                                          working_dir=args.workingDir,
                                          is_test=is_test
                                          )
    # Setup Logging
    setup_logging(config)
    logger = logging.getLogger('visualization_data_describe')

    ### Begin Script ###
    logger.info("Generating an interactive interface for getting single variable descriptive statistics")
    logger.debug("Running Describe Data with arguments: %s" % str(args))

    # Open dataset json
    ds = D3MDataset.from_component_out_file(args.file0)
    logger.debug("Dataset json parse: %s" % str(ds))

    # Add a plot for each valid data column
    columns = ds.get_data_columns()
    data = ds.load_dataset()
    logger.debug(data.head())

    for col in columns:
        logger.debug("Getting column: %s" % col.colName)
        # logger.debug(data[col.colName])





    # Get html to output file path
    out_file_path = path.join(args.workingDir, 
                              config.get('Output', 'out_file')
                              )
    logger.info("Writing output html to: %s" % out_file_path)
    # plot_url = py.offline.plot(plot_data, filename=out_file_path)

