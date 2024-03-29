
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
# import matplotlib
# matplotlib.use("agg")
# import matplotlib.pyplot as plt

from plotly import tools
import plotly as py
import plotly.graph_objs as go

from sklearn.metrics import confusion_matrix

from jinja2 import Environment, PackageLoader, select_autoescape

from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

# Workflow component specific imports
from ls_utilities.ls_logging import setup_logging
from ls_utilities.cmd_parser import get_default_arg_parser
from ls_utilities.ls_wf_settings import SettingsFactory
from ls_utilities.ls_wf_settings import *
from ls_dataset.d3m_dataset import D3MDataset
from ls_dataset.d3m_prediction import D3MPrediction
from ls_problem_desc.ls_problem import ProblemDesc
from ls_problem_desc.d3m_problem import DefaultProblemDesc
from dxdb.dx_db import DXDB

from dxdb.workflow_session import SimpleEDASession
from ls_utilities.dexplorer import *

from modeling.models import *
from modeling.component_out import *


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
    parser = get_default_arg_parser("D3M Compare Model Predictions")
    parser.add_argument('-file0', type=argparse.FileType('r'),
                       help='the dataset json provided for the search')
    args = parser.parse_args()

    if args.is_test is not None:
        is_test = args.is_test == 1
    else:
        is_test = False

    # Get config file
    config = SettingsFactory.get_settings(path.join(args.programDir, 'program', 'settings.cfg'), 
                                          program_dir=args.programDir,
                                          working_dir=args.workingDir,
                                          is_test=is_test)

    dx_config = SettingsFactory.get_dx_settings()

    # Setup Logging
    setup_logging(config)
    logger = logging.getLogger('d3m_vis_describe_data')

    ### Begin Script ###
    logger.info("Generating a series of exploratory data plots for a given dataset")
    logger.debug("Running D3M Describe Data with arguments: %s" % str(args))

    # Open dataset json
    ds = D3MDataset.from_component_out_file(args.file0)
    logger.debug("Dataset json parse: %s" % str(ds))

    # Get User ID and workflow ID
    user_id = args.userId
    logger.debug("User ID: %s" % user_id)
    workflow_id = os.path.split(os.path.abspath(args.workflowDir))[1]
    logger.debug("Workflow ID: %s" % workflow_id)

    # Get connection to db
    logger.debug("DB URL: %s" % dx_config.get_db_backend_url())
    db = DXDB(dx_config.get_db_backend_url())

    # Get connection to UI server
    dex_ui = DexplorerUIServer(dx_config.get_dexplorer_url())

    # Create Workflow Session
    wfs = SimpleEDASession(user_id, workflow_id, "DescribeData")
    wfs = db.add_workflow_session(wfs)
    logger.debug("Workflow Session with id: %s" % str(wfs.__dict__))
    
    # Add dataset to db 
    dsid = db.insert_dataset_metadata(ds)
    ds._id = str(dsid)
    logger.debug("Inserted dataset to db with id: %s" % ds._id)
    wfs.set_dataset(ds)
    db.update_workflow_session(wfs, ['dataset_id'])

    # get Connection to Dexplorer Service
    dex = Dexplorer(dx_config.get_dexplorer_url())
    logger.debug("Dexplorer url: %s" % dex.get_eda_url(wfs._id))


    # Get Viz Factory
    viz_server = VizServer(dx_config.get_viz_server_url())
    viz_factory = VizFactory(viz_server, wfs)
    logger.debug("got viz factory")


    for dr in ds.dataResources:
        logger.debug("Data resource type: %s" % dr.resType)
        if dr.resType.lower() == "table":
            logger.info("Proccessing data resource table with ID: %s" % dr.resID)
            columns = []

            for col in dr.columns:
                # Generate Viz for each column
                viz = viz_factory.generate_simple_eda_viz(ds, dr, col)
                if viz is not None:
                    viz = db.add_viz(viz)
                    wfs.add_viz(viz)

                # Ignore index columns
                if ('index' not in col.colName.lower()) and \
                        ('id' not in col.colName.lower()):
                    # logger.debug("Processing columns with name: %s" % col.colName)
                    if any([col.colType == ctype for ctype in ['integer', 'real']]):
                        logger.info("Adding continuous variable: %s\t with type %s" % (col.colName, col.colType))
                        columns.append(col)
                    elif any([col.colType == ctype for ctype in ['categorical']]):
                        logger.info("Adding categorical variable: %s" % col.colName)
                        columns.append(col)

            # Loading data for resource
            data_path = path.join(ds.get_ds_path(), dr.resPath)
            logger.debug("Got data path from dataset with ds root path: %s\t total path: %s" % (ds.get_ds_path(), data_path))
            data = pd.read_csv(data_path, sep=',')
            logger.debug(data.head())
            logger.info("Adding charts for %i columns" % len(columns))
            num_plots = len(columns)
            titles = tuple(col.colName for col in columns)
            fig = tools.make_subplots(rows=num_plots, cols=1,
                                      subplot_titles=titles)
            dim = 600
            height = dim * num_plots
            fig['layout'].update(height=height, width=dim)

            for i, col in enumerate(columns):
                if any([col.colType == ctype for ctype in ['integer', 'real']]):
                    logger.debug("Adding histogram for continuous variable")
                    fig.append_trace(go.Histogram(x=data.loc[:,col.colName], 
                                                name=col.colName),
                        i + 1, 1)

                elif any([col.colType == ctype for ctype in ['categorical']]):
                    logger.debug("*****************************************")
                    logger.debug("Adding bar chart for categorical variable")
                    d = data[col.colName].value_counts()
                    xdata = list(d.keys())
                    ydata = [d[key] for key in xdata]
                    logger.info("counts: %s" % str(d))
                    logger.info("Keys: %s" % str(xdata))
                    logger.info("values: %s" % str(ydata))

                    fig.append_trace(go.Bar(x=xdata,
                                            y=ydata,
                                            name=col.colName),
                        i + 1, 1)



    # Go through each tabular data resource
    # data_resource = None
    # for dr in ds.dataResources:
        # if dr.resID == ptarget.resource_id:
            # data_resource = dr
            # logger.debug("Got Data resourse\n%s" % str(data_resource))
    # if data_resource is None:
        # logger.error("No matching data resouce was found for info from problem\n%s" % str(ptarget))
    # Get column info
    # target_col = None
    # for col in dr.columns:
        # logger.debug("Comparing to columns: %s" % str(col))
        # if col.colIndex == ptarget.column_index:
            # logger.debug("Found matching for %s column with %s column" % (ptarget.column_name, col.colName))
            # target_col = col	

    # logger.debug("Target col: %s" % str(target_col))
    # coltype = target_col.colType
    # plot_type = None
    # if any([coltype.lower() == ctype for ctype in ['integer', 'real']]):
        # logger.info("Data is numeric, using scatter plots")
        # plot_type = "scatter"
    # else:
        # logger.info("Data is not numeric. Using confusion matric")
        # plot_type = "confusion matrix"

    # Setup subplots
    # num_plots = pred_data.shape[1] - 2
    # fig = tools.make_subplots(rows=num_plots, cols=1)
    # plots = []

    # # Iterate over columns of predictions
    # logger.debug("Columns: %s" % str(pred_data.columns))
    # truth_col = pred_data.columns[1]
    # np.set_printoptions(precision=2)
    # for i, col in enumerate(pred_data.columns[2:]):
        # logger.info("Generating plot for columns:\t %s" % col)
	
	# # pdata = pred_data.loc[:,truth_col + [col]]
    # if plot_type == "scatter":
        # fig.append_trace(go.Scatter(
        # x=pred_data.loc[:,truth_col],
        # y=pred_data.loc[:,col],
        # mode='markers'),
        # i + 1, 1)
    # else:
        # # Compute confusion matrix
        # data_labels = pred_data[truth_col].unique()
        # cm = confusion_matrix(pred_data[truth_col], pred_data[col], 
                # labels=data_labels)
        # logger.debug("Confusion Matrix: %s" % str(cm))
        # logger.debug("Data Labels: %s" % str(data_labels))
        # fig.append_trace(go.Heatmap(z=cm),
            # i + 1, 1)   
		




    # logger.debug("############################################")
    # # Import data csv into pandas dataframe
    # for dr in ds.dataResources:
        # if dr.resType == 'table':
            # dspath = path.join(ds.get_ds_path(), dr.resPath)
            # logger.debug("Getting data csv: %s" % dspath)
            # data = pd.read_csv(dspath, ',', index_col=0)
            # # logger.debug(data.head())
            # # logger.debug(data.shape)
            # break

    # # Import prediction result csv into pandas dataframe
    # ppath = path.join(ds.ppath, ds.pfiles[0])
    # logger.debug("Importing prediction data at: %s" % ppath)
    # pdata = pd.read_csv(ppath, ',', index_col=0)
    # pcol = pdata.columns[0]
    # pdata.rename(columns={pcol: pcol + "_pred"}, inplace=True)

    # # Merge data and prediciton csv
    # merged = data.merge(pdata, how='left', left_index=True, right_index=True)
    # logger.debug("Merged data: %s" % str(merged.shape))

    
    # Isolate prediction and predicted column with id
    # logger.debug(merged.loc[:, [pcol, pcol + "_pred"]].head())
    # out_data = merged.loc[:, [pcol, pcol + "_pred"]]

    ### Create Confusion Matrix ###
    # cm = confusion_matrix(out_data[pcol], out_data[pcol + '_pred'])
    # np.set_printoptions(precision=2)

    # Plot confusion Matrix
    # fig = plt.figure()
    # class_names = out_data[pcol].unique()
    # plot_confusion_matrix(cm, classes=class_names, normalize=True, title='Normalized confusion matrix')

    # Copy support library files to output directory
    # srcdir = path.join(args.programDir, 'program', 'html','lib')
    # outdir = path.join(args.workingDir, 'lib')
    # logger.debug("Copying files from %s" % srcdir)
    # if path.isdir(outdir):
	# rmtree(outdir)
    # copytree(srcdir, outdir)

    # Copy support html documents to output file
    # srcdir = path.join(args.programDir, 'program', 'html','resources')
    # outdir = path.join(args.workingDir, 'resources')
    # logger.debug("Copying files from %s" % srcdir)
    # if path.isdir(outdir):
	# rmtree(outdir)
    # copytree(srcdir, outdir)

    # Write data to output directory
    # out_file = path.join(args.workingDir, 'resources','data', 'data.csv')
    # out_data.to_csv(out_file,sep=',')

    # Write plot to file
    # fig_path = path.join(args.workingDir, 'resources', 'plot.png')
    # fig.savefig(fig_path)

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
   

    logger.debug("Simple EDA Session in db: \n%s" % str(wfs.__dict__))
    db.update_workflow_session(wfs, ['visualizations'])

    # Get  html to output file path
    out_file_path = path.join(args.workingDir, 
                              config.get('Output', 'out_file')
                              )
    logger.info("Writing output html to: %s" % out_file_path)
    service_url = dex_ui.get_simple_eda_ui_url(wfs)
    wfs.set_session_url(service_url)
    db.update_workflow_session(wfs, ['session_url'])
    logger.debug("Embedded iframe url: %s" % service_url)
    out_html = '<iframe src="http://%s" width="1024" height="768"></iframe>' % service_url
    with open(out_file_path, 'w') as out_file:
        out_file.write(out_html)

