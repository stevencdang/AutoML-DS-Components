
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
import pandas as pd


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
# from ls_workflow.workflow import Workflow as Solution
from modeling.models import Model
from modeling.component_out import *
from modeling.scores import *


__version__ = '0.1'


if __name__ == '__main__':
    # Parse argumennts
    parser = get_default_arg_parser("Model Rank")
    parser.add_argument('-metric', type=str,
                       help='the metric to use to compare the models')
    parser.add_argument('-file0', type=argparse.FileType('r'),
                       help='the dataset json provided for the search')
    parser.add_argument('-file1', type=argparse.FileType('r'),
                       help='the set of models to score')
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
    logger = logging.getLogger('model_rank')

    ### Begin Script ###
    logger.info("Scoring models with selected metric")
    logger.debug("Running Model Rank with arguments: %s" % str(args))

    # Open dataset json to use for scoring
    ds = D3MDataset.from_component_out_file(args.file0)
    logger.debug("Dataset json parse: %s" % str(ds))

    # Decode the models from file
    logger.debug("Model file input: %s" % args.file1)
    m_index, models = ModelSetIO.from_file(args.file1)

    # Init the server connection
    address = config.get_ta2_url()
    name = config.get_ta2_name()
    
    # Crete the metric(s) to use in the score request
    logger.info("using server at address %s" % address)
    if is_test:
        serv = TA2Client(address, debug=True, out_dir=args.workingDir, 
                name=name)
    else:
        serv = TA2Client(address, 
                name=name)
   
    # Create the metric(s) to use in the score request
    metric = Metric(args.metric)

    # Get Score for each solution
    req_ids = {}
    for mid in models:
        model = models[mid]
        req_ids[mid] = serv.score_solution(model, ds, metrics=[metric])
    scores = {}
    for mid in req_ids:
        results = serv.get_score_solution_results(req_ids[mid])
        scores[mid] = ModelScores(models[mid].id, [ds.get_schema_uri()], [Score.from_protobuf(result) for result in results])


    ### Parse through model scores to get dataframe of scores
    # Determine number of scores to  plot:
    sample_scores = len(scores[m_index[0]].scores)
    score_data = {score.metric.type: [] for score in scores[m_index[0]].scores}
    score_data['model_id'] = []
    score_data['model_num'] = []
    metrics = [score.metric.type for score in scores[m_index[0]].scores]
    score_data['index'] = range(len(m_index))

    for mid in scores:
        score_set = scores[mid]
        logger.debug("Adding score data for model with id: %s" % score_set.mid)
        score_data['model_id'].append(mid)
        score_data['model_num'].append(m_index[m_index.index(mid)])
        for score in score_set.scores:
            metric_val = list(score.value.value.values())[0]
            logger.debug("appending score for metric: %s\tvalue: %s" % 
                    (score.metric.type, metric_val))
            logger.debug("Score value tyep: %s" % type(metric_val))
            score_data[score.metric.type].append(metric_val)
            
    data = pd.DataFrame(score_data)
    logger.debug("Converted Score data to dataframe: %s" % str(data.head(20)))
    logger.debug("###############################################")
    logger.debug(data.columns)
    logger.debug(data.shape)
    logger.debug(data.head)
    logger.debug("###############################################")
    # Sort models by metric
    sorted_data = data.sort_values(by=[metrics[0]])
    logger.debug("###############################################")
    logger.debug(sorted_data.columns)
    logger.debug(sorted_data.shape)
    logger.debug(sorted_data)
    logger.debug("###############################################")
    logger.debug(sorted_data[metrics[0]])
    logger.debug(sorted_data['index'])
    sorted_data['rank'] = range(1, sorted_data.shape[0] + 1)
    logger.debug(sorted_data[['rank', metrics[0], 'model_id']])


        

    

        
    out_file_path = path.join(args.workingDir, config.get('Output', 'out_file'))
    ModelRankSetIO.to_file(out_file_path, scores, models, m_index)
