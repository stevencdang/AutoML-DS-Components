
# Author: Steven C. Dang

# Main script for runnign a pipeline search on the DARPA D3M system


from __future__ import absolute_import, division, print_function

import grpc
import logging
import json
import sys
from os import path
import argparse
import pprint
import csv

# Workflow component specific imports
from ls_utilities.ls_logging import setup_logging
from ls_utilities.cmd_parser import get_default_arg_parser
from ls_utilities.ls_wf_settings import Settings as stg
from ls_dataset.d3m_dataset import D3MDataset
from ls_dataset.d3m_prediction import D3MPrediction
from d3m_ta2.ta2_v3_client import TA2Client
from modeling.models import Model, ModelScores


__version__ = '0.1'

logging.basicConfig()


if __name__ == '__main__':
    # Parse argumennts
    parser = get_default_arg_parser("Fit Models")
    parser.add_argument('-file0', type=argparse.FileType('r'),
                       help='the dataset json provided for the search')
    parser.add_argument('-file1', type=argparse.FileType('r'),
                       help='at tab-delimited list of models to fit')
    args = parser.parse_args()

    # Get config file
    config = SettingsFactory.get_settings(path.join(args.programDir, 'program', 'settings.cfg'), 
                                          program_dir=args.programDir,
                                          working_dir=args.workingDir,
                                          is_test=is_test
                                          )

    # Setup Logging
    setup_logging(config)
    logger = logging.getLogger('d3m_pipeline_search')

    ### Begin Script ###
    logger.info("Fitting models using given dataset")
    logger.debug("Fitting models with arguments: %s" % str(args))

    # Open dataset json
    ds = D3MDataset.from_json(args.file0)
    logger.debug("Dataset: %s" % str(ds))

    # Import all the models
    reader = csv.reader(args.file1, delimiter='\t')
    rows = [row for row in reader]
    models =  {mid: Model.from_json(rows[1][i]) for i, mid in enumerate(rows[0])}
    scores =  {mid: ModelScores.from_json(rows[2][i]) for i, mid in enumerate(rows[0])}
    logger.info("Got %i models to fit" % len(models))
    # Print sampel model
    mid = list(models.keys())[0]
    model = models[mid]
    logger.debug("Sample model id: %s\nmodel: \t%s" % (mid, models))

    # Init the server connection
    address = config.get("TA2", 'ta2_url')
    
    logger.info("using server at address %s" % address)
    serv = TA2Client(address)
    
    # Get fitted solution
    serv.hello()

    fit_req_ids = {}
    for mid, model in models.items():
        logger.debug("Fitting model: %s" % str(model))
        fit_req_ids[mid] = serv.fit_solution(model, ds)
    for mid, rid in fit_req_ids.items():
        models[mid].fit = serv.get_fit_solution_results(rid)

    # serv.end_search_solutions(search_id)

    
    # # Write model fit id info to output file
    out_file_path = path.join(args.workingDir, config.get('Output', 'out_file'))
    with open(out_file_path, 'w') as out_file:
        writer = csv.writer(out_file, delimiter='\t')
        writer.writerow([model.id for model in models])
        writer.writerow([str(model.model) for model in models])
        writer.writerow([model.fit for model in models])


