
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

from google.protobuf import json_format

# Workflow component specific imports
from ls_utilities.ls_logging import setup_logging
from ls_utilities.cmd_parser import get_default_arg_parser
from ls_utilities.ls_wf_settings import *
from ls_dataset.d3m_dataset import D3MDataset
from ls_dataset.d3m_prediction import D3MPrediction
from ls_problem_desc.ls_problem import ProblemDesc
from ls_problem_desc.d3m_problem import DefaultProblemDesc
from d3m_ta2.ta2_v3_client import TA2Client
from d3m_eval.summer_2018.prob_discovery import ProblemDiscoveryWriter
# from ls_workflow.workflow import Workflow as Solution
from modeling.models import *
from modeling.component_out import *


__version__ = '0.1'


if __name__ == '__main__':
    # Parse argumennts
    parser = get_default_arg_parser("Model Search")
    parser.add_argument('-file0', type=argparse.FileType('r'),
                       help='the dataset json provided for the search')
    parser.add_argument('-file1', type=argparse.FileType('r'),
                       help='the problem json provided for the search')
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
    logger = logging.getLogger('model_search')

    ### Begin Script ###
    logger.info("Running Pipeline Search on TA2")
    logger.debug("Running D3M Pipeline Search with arguments: %s" % str(args))

    # Open dataset json
    ds = D3MDataset.from_component_out_file(args.file0)
    logger.debug("Dataset json parse: %s" % str(ds))

    # Get the Problem Doc to forulate the Pipeline request
    logger.debug("Problem input: %s" % args.file1)
    prob = ProblemDesc.from_file(args.file1)
    logger.debug("Got Problem Description: %s" % prob.print())

    # Init the server connection
    address = config.get_ta2_url()
    name = config.get_ta2_name()
    
    logger.info("using server at address %s" % address)
    if is_test:
        serv = TA2Client(address, debug=True, out_dir=args.workingDir, 
                name=name)
    else:
        serv = TA2Client(address, 
                name=name)

    if config.get_mode() == 'D3M':
        # Write search and problem to file for problem discovery task
        logger.debug("Writing to out_dir: %s" % config.get_out_path())
        prob_list = ProblemDiscoveryWriter(config.get_out_path())
        # Search for solutions
        search_id, request = serv.search_solutions(prob, ds, get_request=True)
        prob_list.add_problem(prob, request)
    else:
        # Search for solutions
        search_id = serv.search_solutions(prob, ds, get_request=True)
    soln_ids = serv.get_search_solutions_results(search_id)
    if soln_ids is None:
        raise Exception("No solution returned")
    
    # Get Model for each solution returned
    solns = {}
    for soln_id in soln_ids:
        solns[soln_id] = serv.describe_solution(soln_id)
        logger.debug("Got pipeline descripton for solution id %s: \n%s" % (soln_id, str(solns[soln_id])))

    ### Temp patch of writing to file and reading back in to simulate passing between components
    out_file_name = "model_data.tsv"

    out_file_path = path.join(args.workingDir, out_file_name)
    ModelSetIO.to_file(out_file_path, solns)
    m_index, models = ModelSetIO.from_file(out_file_path)

    # Get fitted solution
    fit_req_ids = {}
    #fitted_models = {}
    fitted_results = {}
    for mid, model in models.items():
        logger.debug("Fitting model: %s" % str(model))
        fit_req_ids[mid] = serv.fit_solution(model, ds)
    for mid, rid in fit_req_ids.items():
        logger.debug("Model id: %s\tfit model request id: %s" % (mid, rid))
        models[mid].fitted_id, fitted_results[mid] = serv.get_fit_solution_results(rid)

    for mid in models:
        logger.debug("Got fitted model with model id: %s" % mid)
        logger.debug("Model: %s\tFitted Model: %s" % (mid, models[mid].fitted_id))
    
        
    # # Write model fit id info to output file
    out_file_path = path.join(args.workingDir, config.get('Output', 'out_file'))

    FittedModelSetIO.to_file(out_file_path, models, m_index)

    # Write dataset info to output file
    out_file_path = path.join(args.workingDir, config.get('Output', 'dataset_out_file'))
    ds.to_component_out_file(out_file_path)
    if args.is_test == 1:
        # Write out human readable version for debugging
        ds.to_json_pretty(out_file_path + '.readable')

    # Write Solution workflows to file



