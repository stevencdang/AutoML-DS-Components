
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

# Workflow component specific imports
from ls_utilities.ls_logging import setup_logging
from ls_utilities.cmd_parser import get_default_arg_parser
from ls_utilities.ls_wf_settings import Settings as stg
from ls_dataset.d3m_dataset import D3MDataset
from ls_dataset.d3m_prediction import D3MPrediction
from ls_problem_desc.ls_problem import ProblemDesc
from ls_problem_desc.d3m_problem import D3MProblemDesc
from d3m_ta2.ta2_v3_client import TA2Client


__version__ = '0.1'

logging.basicConfig()

class Solution(object):

    def __init__(self, sid):
        self.sid = sid
        self.workflow = None
        self.steps = None
        self.scores = None
    
    def add_description(self, workflow, step_desc):
        self.workflow = workflow
        self.steps = step_desc


if __name__ == '__main__':
    # Parse argumennts
    parser = get_default_arg_parser("D3M Pipeline Search")
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
    logger = logging.getLogger('d3m_pipeline_search')

    ### Begin Script ###
    logger.info("Running Pipeline Search on TA2")
    logger.debug("Running D3M Pipeline Search with arguments: %s" % str(args))

    # Open dataset json
    ds = D3MDataset.from_json(args.file0)
    logger.debug("Dataset json parse: %s" % str(ds))

    # Get the Problem Doc to forulate the Pipeline request
    prob_desc = ProblemDesc.from_json(
        ProblemDesc.get_default_problem(ds))
    logger.debug("Got Problem Description for json: %s" % prob_desc.print())
    prob = D3MProblemDesc.from_problem_desc(prob_desc)
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
    # for soln_id in solns:
        # slns[soln_id].add_description(*self.serv.describe_solution(soln_id))

    # Get Score for each solution
    score_req_ids = []
    for soln_id in solns:
        score_req_ids.append(serv.score_solution(soln_id, ds))
    scores = {}
    for req_id in score_req_ids:
        scores[req_id] = serv.get_score_solution_results(req_id)

    # serv.end_search_solutions(search_id)

    # ### For testing only ###
    # serv.hello()
    # serv.list_primitives()

    # search_id = serv.search_solutions(prob, ds)
    # soln_ids = serv.get_search_solutions_results(search_id)
    # if soln_ids is None:
        # raise Exception("No solution returned")
    fit_req_ids = []
    for soln_id in soln_ids:
        fit_req_ids.append(serv.fit_solution(soln_id, ds))
    # for fit_req_id in fit_req_ids:

    

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
    
    # Write dataset info to output file
    out_file_path = path.join(args.workingDir, config.get('Output', 'data_out_file'))
    ds.to_json(out_file_path)
    # Write out human readable version for debugging
    ds.to_json_pretty(out_file_path + ".readable")

    # Write Solution workflows to file



