
# Author: Steven C. Dang

# Main script for generating a confusion matrix viz taking in a d3m dataset and a prediction


import logging
import sys
from os import path
import os
import argparse
import itertools
from shutil import copytree, rmtree, copyfile
import requests

# import pandas as pd
# import numpy as np
# import matplotlib
# matplotlib.use("agg")
# import matplotlib.pyplot as plt
# from sklearn.metrics import confusion_matrix

from jinja2 import Environment, PackageLoader, select_autoescape

# Workflow component specific imports
from ls_utilities.ls_logging import setup_logging
from ls_utilities.cmd_parser import get_default_arg_parser
from ls_utilities.ls_wf_settings import *

from ls_dataset.d3m_dataset import D3MDataset
from modeling.models import *
from modeling.scores import *

__version__ = '0.1'


class LS_Path_Factory(object):

    def __init__(self, workingDir, programDir):
        self.workingDir = workingDir
        self.programDir = programDir

    def get_out_path(self, fpath):
        return path.join(self.workingDir, fpath)

    def get_hosted_path(self, fpath):
        return "LearnSphere?htmlPath=" + self.get_out_path(fpath)


if __name__ == '__main__':
    # Parse argumennts
    parser = get_default_arg_parser("Compare Model Scores")
    parser.add_argument('-file0', type=argparse.FileType('r'),
                       help='the scores for the model to render in a boxplot')
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
    logger = logging.getLogger('compare_model_scores')

    ### Begin Script ###
    logger.info("Generating an interactive interface for getting single variable descriptive statistics")
    logger.debug("Running Describe Data with arguments: %s" % str(args))

    # Get html from Viz Server
    server_addr = "http://glacier.andrew.cmu.edu:8050"
    viz_url = server_addr + "/viz/viz1"
    html = requests.get(viz_url)

    # Write html to output file
    out_file_path = path.join(args.workingDir, 
                              config.get('Output', 'out_file')
                              )
    logger.info("Writing output html to: %s" % out_file_path)
    with open(out_file_path, 'w') as out_file:
        out_file.write(html.text)
    

    # Generate html from template and write to output file
    # path_factory = LS_Path_Factory(args.workingDir, args.programDir)
    # env = Environment(
        # loader=PackageLoader("ls_iviz", "templates"),
        # autoescape=select_autoescape(['html'])
    # )
    # template_info = {
        # 'resource_path': path_factory.get_hosted_path(
            # path.join('resources')),
        # 'viz_img_path': path_factory.get_hosted_path(
            # path.join('resources', 'plot.png')),
        # 'raw_data': cm.tolist(),
        # 'data_classes': str([str(cls) for cls in class_names]),
        # 'd3_dashboard_css': env.get_template('dashboard.css').render(),
        # 'component_css': env.get_template('confusion_matrix.css').render(),
        # 'component_js': env.get_template('confusion_matrix.js').render(),
    # }
    # viz_template = env.get_template("confusion_matrix.html")
    # out_file_path = path.join(args.workingDir, 
                              # config.get('Output', 'out_file')
                              # )
    # logger.info("Writing output html to: %s" % out_file_path)
    # with open(out_file_path, 'w') as out_file:
        # out_file.write(viz_template.render(template_info))
    

    # Write output html to file
    # src_html = path.join(args.programDir, 'program', 'html', 'index.html')
    # out_file_path = path.join(args.workingDir, config.get('Output', 'out_file'))
    # logger.info("Writing output html to: %s" % out_file_path)
    # copyfile(src_html, out_file_path)
