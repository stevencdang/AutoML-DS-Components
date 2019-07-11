
# Author: Steven C. Dang

# Main script for importing provided D3M dataset schemas for operation on datasets

import logging
import os.path as path
import os
import csv

# Workflow component specific imports
from ls_utilities.ls_logging import setup_logging
from ls_utilities.cmd_parser import get_default_arg_parser
from ls_utilities.ls_wf_settings import *
from ls_dataset.d3m_dataset import D3MDataset
from user_ops.dataset import DatasetImporter
from dxdb.dx_db import DXDB
from dxdb.workflow_session import SimpleEDASession

__version__ = '0.1'

if __name__ == '__main__':

    # Parse argumennts
    parser = get_default_arg_parser("Import List of available D3M Datasets")
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
    # Get config for dx services
    dx_config = SettingsFactory.get_dx_settings()

    # Setup Logging
    setup_logging(config)
    logger = logging.getLogger('datasets_importer')

    ### Begin Script ###
    logger.info("Importing List of available datasets")
    logger.debug("Running Dataset Importer with arguments: %s" % str(args))

    # Get connection to db
    logger.debug("DB URL: %s" % dx_config.get_db_backend_url())
    db = DXDB(dx_config.get_db_backend_url())

    # Get Session Metadata
    user_id = args.userId
    logger.debug("User ID: %s" % user_id)
    workflow_id = os.path.split(os.path.abspath(args.workflowDir))[1]
    logger.debug("Workflow ID: %s" % workflow_id)
    comp_type = os.path.split(os.path.abspath(args.toolDir))[1]
    logger.debug("Component Type: %s" % comp_type)
    comp_id = os.path.split(os.path.abspath(args.componentXmlFile))[1].split(".")[0]
    logger.debug("Component Id: %s" % comp_id)

    # Start new session
    # session = ImportDatasetSession(

    # Read in the dataset json
    ds_root = config.get_dataset_path()
    runner = DatasetImporter()
    # datasets = runner.run(ds_root)


    # Write dataset info to output file
    out_file_path = path.join(args.workingDir, config.get('Dataset', 'out_file'))
    logger.info("Writing dataset list of %i datasets to file: %s" % (len(datasets), out_file_path))
    with open(out_file_path, 'w') as out_file:
        out_csv = csv.writer(out_file, delimiter='\t')
        out_csv.writerow(datasets)
