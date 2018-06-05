
# Author: Steven C. Dang

# Main script for importing provided D3M dataset schemas for operation on datasets

import logging
import os.path as path
import sys
import json
import argparse

# Workflow component specific imports
from ls_utilities.ls_logging import setup_logging
from ls_utilities.cmd_parser import get_default_arg_parser
from ls_utilities.ls_wf_settings import Settings as stg
from ls_dataset.d3m_dataset import D3MDataset
from ls_problem_desc.d3m_problem import D3MProblemDesc
from ls_problem_desc.ls_problem import ProblemDesc

__version__ = '0.1'

logging.basicConfig()

if __name__ == '__main__':

    # Parse argumennts
    parser = get_default_arg_parser("Generate Default Problem")
    parser.add_argument('-file0', type=argparse.FileType('r'),
                       help='the dataset json provided for the search')
    args = parser.parse_args()

    # Get config file
    if args.programDir is None:
        config = stg()
    else:
        config = stg(path.join(args.programDir, 'program', 'settings.cfg'))

    # Setup Logging
    setup_logging(config.parse_logging(), args.workingDir, args.is_test == 1)
    logger = logging.getLogger('problem_generator_default')

    ### Begin Script ###
    logger.info("Generating Problem Statement based on default problem for given dataset")
    logger.debug("Running Generate Default Problem with arguments: %s" % str(args))

    # Open dataset json
    ds = D3MDataset.from_json(args.file0)
    logger.debug("Dataset json: %s" % str(ds))

    # Get Problem Schema from Dataset
    prob_path = ProblemDesc.get_default_problem(ds)
    prob_desc = ProblemDesc.from_json(prob_path)
    logger.debug("Got Problem Description for json: %s" % prob_desc.print())
    prob = D3MProblemDesc.from_problem_desc(prob_desc)
    logger.debug("Got D3M Problem Description: %s" % prob.print())

    # Write dataset info to output file
    out_file_path = path.join(args.workingDir, config.get('Main', 'out_file'))
    logger.info("Writing dataset json to: %s" % out_file_path)
    prob.to_json(out_file_path)
    if args.is_test == 1:
        prob.to_json_pretty(out_file_path + '.readable')