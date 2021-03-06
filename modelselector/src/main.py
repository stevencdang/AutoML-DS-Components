
# Author: Steven C. Dang

# Main script for importing provided D3M dataset schemas for operation on datasets

import logging
import os.path as path
import sys
import json
import pprint
import argparse
import csv

# Workflow component specific imports
from ls_utilities.ls_logging import setup_logging
from ls_utilities.cmd_parser import get_default_arg_parser
from ls_utilities.ls_wf_settings import *
from ls_dataset.d3m_dataset import D3MDataset
from modeling.models import *
from modeling.component_out import *

__version__ = '0.1'

if __name__ == '__main__':

    # Parse argumennts
    parser = get_default_arg_parser("Select Model")
    parser.add_argument('-model_id', type=str,
                       help='the name of the dataset to import')
    parser.add_argument('-file0', type=argparse.FileType('r'),
                       help='the tab-separated list of models to select from')
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
    logger = logging.getLogger('model_selector')

    ### Begin Script ###
    logger.info("Outputing model selected by user")
    logger.debug("Running Model Selector with arguments: %s" % str(args))

    if args.is_test is not None:
        is_test = args.is_test == 1
    else:
        is_test = False

    # Decode the models from file
    logger.debug("Model file input: %s" % args.file0)
    m_index, models = ModelSetIO.from_file(args.file0)
    
    selected_mid = m_index[int(args.model_id)]
    model = models[selected_mid]
    logger.debug("Seleted Model ID:\t %s" % selected_mid)
    logger.debug("Seleted Model:\t%s" % str(model.to_dict()))

    # Write dataset info to output file
    out_file_path = path.join(args.workingDir, config.get('Output', 'out_file'))
    out_data = model.to_dict()
    with open(out_file_path, 'w') as out_file:
        json.dump(out_data, out_file)
