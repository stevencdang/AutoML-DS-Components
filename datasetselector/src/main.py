
# Author: Steven C. Dang

# Main script for importing provided D3M dataset schemas for operation on datasets

import logging
import os.path as path
import sys
import json
import pprint

# Workflow component specific imports
from ls_utilities.ls_logging import setup_logging
from ls_utilities.cmd_parser import get_default_arg_parser
from ls_utilities.ls_wf_settings import Settings as stg
from ls_dataset.d3m_dataset import D3MDataset

__version__ = '0.1'

logging.basicConfig()

if __name__ == '__main__':

    # Parse argumennts
    parser = get_default_arg_parser("Import D3M Dataset")
    parser.add_argument('-ds_name', type=str,
                       help='the name of the dataset to import')
    args = parser.parse_args()

    # Get config file
    if args.programDir is None:
        config = stg().parse_config()
    else:
        config = stg(path.join(args.programDir, 'program', 'settings.cfg')).parse_config()

    # Setup Logging
    setup_logging(config, args.workingDir, args.is_test == 1)
    logger = logging.getLogger('d3m_dataset_selector')

    ### Begin Script ###
    logger.info("Importing D3M Dataset selected by user")
    logger.debug("Running Dataset Import with arguments: %s" % str(args))

    # Get selected dataset name
    if args.ds_name is not None:
        ds_name = args.ds_name
    else:
        ds_name = "185_baseball"

    # Read in the dataset json
    ds_path = path.join(config['dataset_dir'], ds_name)
    schema_path = D3MDataset.get_schema_path(ds_path)
    with open(schema_path, 'r') as spath:
        logger.debug("opening dataset schema at path: %s" % schema_path)
        ds_data = json.load(spath)
    logger.debug("using json: %s" % str(ds_data)) 
    ds = D3MDataset(ds_path, ds_data)
    logger.debug("Got dataset: %s" % str(ds))

    # Write dataset info to output file
    out_file_path = path.join(args.workingDir, config['out_file'])
    logger.info("Writing dataset json to: %s" % out_file_path)
    ds.to_json(out_file_path)
    # ds_json = json.loads(ds.to_json())
    # with open(out_file_path, 'w') as out_file:
        # pprint.pprint(ds_json, out_file)
