
# Author: Steven C. Dang

# Convenience class and functions for supporting parsing cmd line inputs
# when running Workflow components

import logging
import argparse
import os.path as path


# logging.basicConfig()
logger = logging.getLogger(__name__)

def get_session_info(my_args):
    # Get Session Metadata

    working_dir = my_args.workingDir.split(path.sep)[1:]
    user_id = my_args.userId
    logger.debug("User ID: %s" % user_id)
    workflow_id = working_dir[-3]
    logger.debug("Workflow ID: %s" % workflow_id)
    comp_type = path.split(path.abspath(my_args.programDir))[1]
    logger.debug("Component Type: %s" % comp_type)
    comp_id = working_dir[-2]
    logger.debug("Component Id: %s" % comp_id)

    return user_id, workflow_id, comp_type, comp_id


def get_default_arg_parser(desc):
    """
    Define an argument parser for use with Tigris Components and
    mandatory arguments

    """
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-programDir', type=str,
                       help='the component program directory')

    parser.add_argument('-workingDir', type=str,
                       help='the component instance working directory')

    parser.add_argument('-userId', type=str,
                       help='the user id')

    parser.add_argument('-workflowDir', type=str,
                       help='the workflow directory')

    parser.add_argument('-toolDir', type=str,
                       help='the main directory of the component')

    parser.add_argument('-componentXmlFile', type=str,
                       help='a fake path to a component xml file for this instance of the component')


    # For local testing outside of Tigris env
    parser.add_argument('-is_test', type=int,
                       help='set to any integer to indicate this script is being  \
                       run outside a Tigris Workflow')
    return parser


