
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
# from ls_problem_desc.ls_problem import ProblemDesc
# from ls_problem_desc.d3m_problem import D3MProblemDesc
from ls_workflow.workflow import Workflow
from d3m_ta2.ta2_v3_client import TA2Client


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
    if args.programDir is None:
        config = stg()
    else:
        config = stg(path.join(args.programDir, 'program', 'settings.cfg'))

    # Setup Logging
    setup_logging(config.parse_logging(), args.workingDir, args.is_test == 1)
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
    models =  {mid: Workflow.from_json(rows[1][i]) for i, mid in enumerate(rows[0])}
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
        fit_req_ids[mid] = serv.fit_solution(model, ds)
    for mid, rid in fit_req_ids.items():
        models[mid].fit = serv.get_fit_solution_results(rid)

    serv.end_search_solutions(search_id)

    
    # Retrieve output
    # pfiles = set()
    # for pred in predictions:
        # pfiles.add(path.split(pred.predict_result_uri)[-1])


    # ds_data = {'about': ds.about,
               # 'dataResources': [json.loads(dr.to_json()) for dr in ds.dataResources]
               # }
    # logger.debug("Getting problem description in dataset dir: %s" % ds.dpath)
    # pred_out = D3MPrediction(ds.dpath, 
                             # ds_data, 
                             # path.join(ds.get_ds_path(), 'output'), 
                             # prob_desc=prob_desc, 
                             # pfiles=list(pfiles))
    
    # # Write dataset info to output file
    # out_file_path = path.join(args.workingDir, config.get('Output', 'out_file'))
    # pred_out.to_json(out_file_path)
    # Write out human readable version for debugging
    # ds_json = json.loads(pred_out.to_json())
    # with open(out_file_path, 'w') as out_file:
        # pprint.pprint(ds_json, out_file)


