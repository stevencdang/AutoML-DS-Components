
# Author: Steven C. Dang

# Main script for generating a confusion matrix viz taking in a d3m dataset and a prediction


import logging
import sys
from os import path
import os
import argparse
from shutil import copytree, rmtree, copyfile

# Workflow component specific imports
from ls_utilities.ls_logging import setup_logging
from ls_utilities.cmd_parser import get_default_arg_parser
from ls_utilities.ls_wf_settings import Settings as stg
from ls_dataset.ls_prediction import LSPrediction

__version__ = '0.1'

logging.basicConfig()
logger = logging.getLogger('d3m_vis_confusion_matrix')


if __name__ == '__main__':
    # Parse argumennts
    parser = get_default_arg_parser("D3M Visualize Confusion Matrix")
    parser.add_argument('-file0', type=argparse.FileType('r'),
                       help='the dataset json including pipeline search result')
    args = parser.parse_args()

    # Get config file
    if args.programDir is None:
        config = stg()
    else:
        config = stg(path.join(args.programDir, 'program', 'settings.cfg'))

    # Setup Logging
    logger = setup_logging(logger, config.parse_logging(), args.workingDir, args.is_test == 1)

    ### Begin Script ###
    logger.info("Generating a Confusion Matrix on the D3M Pipeline Result")
    logger.debug("Running D3M Visualize Confusion Matrix with arguments: %s" % str(args))

    # Open dataset prediction json
    ds = LSPrediction.from_json(args.file0)
    logger.debug("Dataset json parse: %s" % str(ds))

    # Copy support library files to output directory
    srcdir = path.join(args.programDir, 'program', 'html','lib')
    outdir = path.join(args.workingDir, 'lib')
    logger.debug("Copying files from %s" % srcdir)
    if path.isdir(outdir):
        rmtree(outdir)
    copytree(srcdir, outdir)

    # Copy support html documents to output file
    srcdir = path.join(args.programDir, 'program', 'html','resources')
    outdir = path.join(args.workingDir, 'resources')
    logger.debug("Copying files from %s" % srcdir)
    if path.isdir(outdir):
        rmtree(outdir)
    copytree(srcdir, outdir)

    # Write output html to file
    src_html = path.join(args.programDir, 'program', 'html', 'index.html')
    out_file_path = path.join(args.workingDir, config.get('Output', 'out_file'))
    logger.info("Writing output html to: %s" % out_file_path)
    copyfile(src_html, out_file_path)
