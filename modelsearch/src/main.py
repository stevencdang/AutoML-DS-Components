
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
    ############### TA2 V2 Code #######################
    # server = {
        # 'channel': grpc.insecure_channel(address)
    # }
    # server['stub'] = core_pb2_grpc.CoreStub(server['channel'])
    # server['stub_dataflow_ext'] = dataflow_ext_pb2_grpc.DataflowExtStub(server['channel'])
    # server['stub_data_ext'] = data_ext_pb2_grpc.DataExtStub(server['channel'])
    # server['version'] = core_pb2.DESCRIPTOR.GetOptions().Extensions[
            # core_pb2.protocol_version]
    # ta2 = TA2Client(server)

    # # Execute Pipeline Creation Process
    # context = ta2.start_session()
    # pipelines, predictions = ta2.create_pipelines(ds, prob_desc)
    # ta2.execute_pipelines(ds, pipelines)
    # ta2.end_session()

    ############### End TA2 V2 Code #######################
    serv = TA2Client(address)
    serv.hello()

    search_id = serv.search_solutions(prob, ds)
    soln_ids = serv.get_search_solutions_results(search_id)
    # if soln_ids is None:
        # raise Exception("No solution returned")
    # score_req_ids = []
    # for soln_id in soln_ids:
        # score_req_ids.append(serv.score_solution(soln_id))
    # scores = {}
    # for req_id in score_req_ids:
        # scores[req_id] = serv.get_score_solution_results(req_id)

    # serv.end_search_solutions(search_id)

    # ### For testing only ###
    # serv.hello()
    # serv.list_primitives()

    # search_id = serv.search_solutions(prob, ds)
    # soln_ids = serv.get_search_solutions_results(search_id)
    # if soln_ids is None:
        # raise Exception("No solution returned")
    # fit_req_ids = []
    # for soln_id in soln_ids:
        # fit_req_ids.append(serv.fit_solution(soln_id, ds))
    # for fit_req_id in fit_req_ids:

    

    

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


