
# Author: Steven C. Dang

# Main script for generating a confusion matrix viz taking in a d3m dataset and a prediction


import logging
import sys
from os import path
import os
import argparse
import itertools
from shutil import copytree, rmtree, copyfile

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

from jinja2 import Environment, PackageLoader, select_autoescape

# Workflow component specific imports
from ls_utilities.ls_logging import setup_logging
from ls_utilities.cmd_parser import get_default_arg_parser
from ls_utilities.ls_wf_settings import Settings as stg
from ls_dataset.d3m_prediction import D3MPrediction

__version__ = '0.1'

logging.basicConfig()


class LS_Path_Factory(object):

    def __init__(self, workingDir, programDir):
        self.workingDir = workingDir
        self.programDir = programDir

    def get_out_path(self, fpath):
        return path.join(self.workingDir, fpath)

    def get_hosted_path(self, fpath):
        return "LearnSphere?htmlPath=" + self.get_out_path(fpath)

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, format(cm[i, j], fmt),
                    horizontalalignment="center",
                    color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


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
    setup_logging(config.parse_logging(), args.workingDir, args.is_test == 1)
    logger = logging.getLogger('d3m_vis_confusion_matrix')

    ### Begin Script ###
    logger.info("Generating a Confusion Matrix on the D3M Pipeline Result")
    logger.debug("Running D3M Visualize Confusion Matrix with arguments: %s" % str(args))

    ### Open data and merge to a single file ###
    # Open dataset prediction json
    ds = D3MPrediction.from_json(args.file0)
    logger.debug("Dataset json parse: %s" % str(ds))

    logger.debug("############################################")
    # Import data csv into pandas dataframe
    for dr in ds.dataResources:
        if dr.resType == 'table':
            dspath = path.join(ds.get_ds_path(), dr.resPath)
            logger.debug("Getting data csv: %s" % dspath)
            data = pd.read_csv(dspath, ',', index_col=0)
            # logger.debug(data.head())
            # logger.debug(data.shape)
            break

    # Import prediction result csv into pandas dataframe
    ppath = path.join(ds.ppath, ds.pfiles[0])
    logger.debug("Importing prediction data at: %s" % ppath)
    pdata = pd.read_csv(ppath, ',', index_col=0)
    pcol = pdata.columns[0]
    pdata.rename(columns={pcol: pcol + "_pred"}, inplace=True)

    # Merge data and prediciton csv
    merged = data.merge(pdata, how='left', left_index=True, right_index=True)
    logger.debug("Merged data: %s" % str(merged.shape))

    # Isolate prediction and predicted column with id
    logger.debug(merged.loc[:, [pcol, pcol + "_pred"]].head())
    out_data = merged.loc[:, [pcol, pcol + "_pred"]]

    ### Create Confusion Matrix ###
    cm = confusion_matrix(out_data[pcol], out_data[pcol + '_pred'])
    np.set_printoptions(precision=2)

    # Plot confusion Matrix
    fig = plt.figure()
    class_names = out_data[pcol].unique()
    plot_confusion_matrix(cm, classes=class_names, normalize=True, title='Normalized confusion matrix')

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

    # Write data to output directory
    out_file = path.join(args.workingDir, 'resources','data', 'data.csv')
    out_data.to_csv(out_file,sep=',')

    # Write plot to file
    fig_path = path.join(args.workingDir, 'resources', 'plot.png')
    fig.savefig(fig_path)

    # Generate html from template and write to output file
    path_factory = LS_Path_Factory(args.workingDir, args.programDir)
    env = Environment(
        loader=PackageLoader("ls_iviz", "templates"),
        autoescape=select_autoescape(['html'])
    )
    template_info = {
        'resource_path': path_factory.get_hosted_path(
            path.join('resources')),
        'viz_img_path': path_factory.get_hosted_path(
            path.join('resources', 'plot.png')),
        'raw_data': cm.tolist(),
        'data_classes': str([str(cls) for cls in class_names]),
        'd3_dashboard_css': env.get_template('dashboard.css').render(),
        'component_css': env.get_template('confusion_matrix.css').render(),
        'component_js': env.get_template('confusion_matrix.js').render(),
    }
    viz_template = env.get_template("confusion_matrix.html")
    out_file_path = path.join(args.workingDir, 
                              config.get('Output', 'out_file')
                              )
    logger.info("Writing output html to: %s" % out_file_path)
    with open(out_file_path, 'w') as out_file:
        out_file.write(viz_template.render(template_info))
    

    # Write output html to file
    # src_html = path.join(args.programDir, 'program', 'html', 'index.html')
    # out_file_path = path.join(args.workingDir, config.get('Output', 'out_file'))
    # logger.info("Writing output html to: %s" % out_file_path)
    # copyfile(src_html, out_file_path)
