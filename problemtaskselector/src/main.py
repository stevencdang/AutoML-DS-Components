
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
# from ls_problem_desc.d3m_problem import *
from ls_problem_desc.ls_problem import *

__version__ = '0.1'

logging.basicConfig()

if __name__ == '__main__':

    # Parse argumennts
    parser = get_default_arg_parser("Select Problem Task Select")
    parser.add_argument('-task_name', type=str,
                       help='the task type the user selected')
    parser.add_argument('-file0', type=argparse.FileType('r'),
                       help='the description of the dataset')
    parser.add_argument('-file1', type=argparse.FileType('r'),
                       help='the problem template with target selected')
    args = parser.parse_args()

    # Get config file
    if args.programDir is None:
        config = stg()
    else:
        config = stg(path.join(args.programDir, 'program', 'settings.cfg'))

    # Setup Logging
    setup_logging(config.parse_logging(), args.workingDir, args.is_test == 1)
    logger = logging.getLogger('problem_task_selector')

    ### Begin Script ###
    logger.info("Initializing Problem Description for a dataset with selected column")
    logger.debug("Running Problem Target Selection with arguments: %s" % str(args))

    # Open dataset json
    ds = D3MDataset.from_component_out_file(args.file0)
    logger.debug("Dataset json parse: %s" % str(ds))

    # Initialize a Problem Description and set target info
    prob = ModelingProblem.problem_target_select_from_file(args.file1)
    ###### Maybe add validation logic here? #####
    prob.add_task_type(args.task_name)

    # Write Problem Template with task type and metric options to output file
    out_file_path = path.join(args.workingDir, config.get('Dataset', 'out_file'))
    logger.info("Writing template prob desc to: %s" % out_file_path)
    ModelingProblem.problem_task_select_to_file(prob, out_file_path)
    if args.is_test == 1:
        prob.print(out_file_path + '.readable')