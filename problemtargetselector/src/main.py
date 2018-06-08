
# Author: Steven C. Dang

# Main script for importing provided D3M dataset schemas for operation on datasets

import logging
import hashlib
from datetime import datetime
import os.path as path
import sys
import json
import pprint
import argparse
import csv

# Workflow component specific imports
from ls_utilities.ls_logging import setup_logging
from ls_utilities.cmd_parser import get_default_arg_parser
from ls_utilities.ls_wf_settings import Settings as stg
from ls_dataset.d3m_dataset import D3MDataset
from ls_problem_desc.d3m_problem import *
from ls_problem_desc.ls_problem import ProblemDesc

__version__ = '0.1'

logging.basicConfig()

if __name__ == '__main__':

    # Parse argumennts
    parser = get_default_arg_parser("Select Problem Target")
    parser.add_argument('-target_name', type=str,
                       help='the name of the column from the dataset to use')
    parser.add_argument('-file0', type=argparse.FileType('r'),
                       help='the description of the dataset')
    args = parser.parse_args()

    # Get config file
    if args.programDir is None:
        config = stg()
    else:
        config = stg(path.join(args.programDir, 'program', 'settings.cfg'))

    # Setup Logging
    setup_logging(config.parse_logging(), args.workingDir, args.is_test == 1)
    logger = logging.getLogger('dataset_selector')

    ### Begin Script ###
    logger.info("Initializing Problem Description for a dataset with selected column")
    logger.debug("Running Problem Target Selection with arguments: %s" % str(args))

    # Open dataset json
    ds = D3MDataset.from_component_out_file(args.file0)
    logger.debug("Dataset json parse: %s" % str(ds))

    # Get the information about the selected target from the dataset
    for resource in ds.dataResources:
        if resource.resType == 'table':
            logger.debug("Looking for column in resource: %s" % str(resource))
            cols = resource.columns
            logger.debug("Got resource columns: %s" % str([str(col) for col in cols]))
            col_names = [col.colName for col in cols]
            logger.debug("Got column names: %s" % col_names)
            i = col_names.index(args.target_name)
            target_col = cols[i]
            target_resource = resource
            logger.debug("Got target column from resource with ID, %s, at index %i: %s" % (target_resource.resID, i, str(target_col)))

    if target_col is None:
        raise Exception("Could not identify column with name %s from dataset" % args.target_name)

    # Initialize a Problem Description and set target info
    prob = ProblemDesc()
    prob.desc = "CMU-Tigris User generated problem"
    prob.name = "Problem-%s" % str(datetime.now())
    prob.add_input(ds.id, target_resource, target_col)

    # Cast as DefaultProblemDesc for communication
    prob_out = DefaultProblemDesc.from_problem_desc(prob)

    # Write dataset info to output file
    out_file_path = path.join(args.workingDir, config.get('Dataset', 'out_file'))
    logger.info("Writing template prob desc to: %s" % out_file_path)
    prob_out.to_json(out_file_path)
    if args.is_test == 1:
        prob_out.to_json_pretty(out_file_path + '.readable')
