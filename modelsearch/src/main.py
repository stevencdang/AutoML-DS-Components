
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
from ls_utilities.ls_wf_settings import Settings as stg
from ls_dataset.d3m_dataset import D3MDataset
from ls_dataset.d3m_prediction import D3MPrediction
from ls_problem_desc.ls_problem import ProblemDesc
from ls_problem_desc.d3m_problem import D3MProblemDesc
from d3m_ta2.ta2_v3_client import TA2Client
from ls_workflow.workflow import Workflow as Solution


__version__ = '0.1'

logging.basicConfig()

        



if __name__ == '__main__':
    # Parse argumennts
    parser = get_default_arg_parser("D3M Pipeline Search")
    parser.add_argument('-file0', type=argparse.FileType('r'),
                       help='the dataset json provided for the search')
    parser.add_argument('-file1', type=argparse.FileType('r'),
                       help='the problem json provided for the search')
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
    logger.info("Running Pipeline Search on TA2")
    logger.debug("Running D3M Pipeline Search with arguments: %s" % str(args))

    # Open dataset json
    ds = D3MDataset.from_json(args.file0)
    logger.debug("Dataset json parse: %s" % str(ds))

    # Get the Problem Doc to forulate the Pipeline request
    logger.debug("Problem input: %s" % args.file1)
    prob = D3MProblemDesc.from_file(args.file1)
    logger.debug("Got D3M Problem Description: %s" % prob.print())

    # Init the server connection
    address = config.get("TA2", 'ta2_url')
    
    logger.info("using server at address %s" % address)
    serv = TA2Client(address)
    serv.hello()

    # Search for solutions
    search_id = serv.search_solutions(prob, ds)
    soln_ids = serv.get_search_solutions_results(search_id)
    if soln_ids is None:
        raise Exception("No solution returned")
    
    # Get workflow for each solution returned
    solns = {soln_id: Solution(soln_id) for soln_id in soln_ids}
    for soln_id in solns:
        solns[soln_id].add_description(*serv.describe_solution(soln_id))
        logger.debug("Got pipline descripton for solution id %s: \n%s" % (soln_id, solns[soln_id].model))

    # Get Score for each solution
    score_req_ids = {}
    for soln_id in solns:
        soln = solns[soln_id]
        score_req_ids[soln.id] = serv.score_solution(soln, ds)
    scores = {}
    for sid in score_req_ids:
        solns[sid].score = serv.get_score_solution_results(score_req_ids[sid])

    serv.end_search_solutions(search_id)

    # ### For testing only ###
    # serv.hello()
    # serv.list_primitives()

    # search_id = serv.search_solutions(prob, ds)
    # soln_ids = serv.get_search_solutions_results(search_id)
    # if soln_ids is None:
        # raise Exception("No solution returned")
    # fit_req_ids = {}
    # for sid, soln in solns.items():
        # fit_req_ids[sid] = serv.fit_solution(soln, ds)
    # for sid, rid in fit_req_ids.items():
        # solns[sid].model = serv.get_fit_solution_results(rid)

        

    

    # serv.end_search_solutions(search_id)

    ### End testing code ###
   
    # Write the received solutions to file
    for sid, soln in solns.items():
        logger.debug("###########################################")
        logger.debug("Received solution: %s" % soln)
        logger.debug("###########################################")
    out_file_path = path.join(args.workingDir, config.get('Output', 'workflows_out_file'))
    with open(out_file_path, 'w') as out_file:
        out = csv.writer(out_file, delimiter='\t')
        out.writerow([solns[sln].id for sln in solns])
        out.writerow([str(solns[sln]) for sln in solns])

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
    
    # Write dataset info to output file
    out_file_path = path.join(args.workingDir, config.get('Output', 'dataset_out_file'))
    ds.to_json(out_file_path)
    # Write out human readable version for debugging
    ds.to_json_pretty(out_file_path + ".readable")

    # Write Solution workflows to file



