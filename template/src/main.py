
# Author: Steven C. Dang

# Main script for generating a confusion matrix viz taking in a d3m dataset and a prediction


import logging
import sys
from os import path
import argparse

# Workflow component specific imports
from ls_logging import setup_logging
from cmd_parser import get_default_arg_parser
from ls_wf_settings import Settings as stg
from ls_dataset import LSDataset

__version__ = '0.1'

logging.basicConfig()
logger = logging.getLogger('d3m_vis_confusion_matrix')


if __name__ == '__main__':
    # Parse argumennts
    parser = get_default_arg_parser("D3M Visualize Confusion Matrix")
    parser.add_argument('-file0', type=argparse.FileType('r'),
                       help='the dataset json including pipeline search result')
    args = parser.parse_args()

    # Get config file
    if args.programDir is None:
        config = stg()
    else:
        config = stg(path.join(args.programDir, 'settings.cfg'))

    # Setup Logging
    logger = setup_logging(logger, config.parse_logging(), args.workingDir, args.is_test == 1)

    ### Begin Script ###
    logger.info("Generating a Confusion Matrix on the D3M Pipeline Result")
    logger.debug("Running D3M Visualize Confusion Matrix with arguments: %s" % str(args))

    # Open dataset json
    ds = LSDataset.from_json(args.file0)
    logger.debug("Dataset json parse: %s" % str(ds))


