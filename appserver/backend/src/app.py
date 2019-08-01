
import logging
from logging.config import dictConfig
from flask import Flask, request, render_template, url_for
import flask.logging
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
import re
import sys

import urllib

from ls_utilities.ls_logging import setup_logging
from ls_utilities.ls_wf_settings import *
from ls_dataset.d3m_dataset import D3MDataset
from ls_problem_desc.ls_problem import ProblemDesc
from dxdb.dx_db import DXDB
from dxdb.workflow_session import *

from bokeh.client import pull_session
from bokeh.embed import server_session

from user_ops.modeling import *
from user_ops.problem import *
from user_ops.dataset import *

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

# Configure logging to stdout
logger = logging.getLogger(__name__)
for handler in app.logger.handlers:
    app.logger.removeHandler(handler)
# handler = logging.StreamHandler(stream=sys.stdout)
# app.logger.addHandler(handler)



@app.route('/')
def main():
    logger.debug("Logging with flask logger")
    return "Hello World"

@app.route('/wfs/<string:wfid>', methods = ['GET', 'PUT'])
def get_workflow_session(wfid):
    if request.method == 'GET':
        wfs = db_client.get_workflow_session(wfid)
        logger.debug("workflow session from db: %s" % wfs.to_json())
        return wfs.to_json()
    if request.method == 'PUT':
        data = json.loads(request.data)
        wfs = db_client.get_workflow_session(wfid)
        logger.debug("workflow session from db: %s" % wfs.to_json())
        logger.debug("**************************************")
        for key in data:
            logger.debug("updating key: %s\t to value: %s" % (key, data[key]))
            setattr(wfs, key, data[key])
        logger.debug("workflow session with updated values: %s" % wfs.to_json())
        logger.debug("updated fields: %s" % data.keys())

        db_client.update_workflow_session(wfs, data.keys())
        return "Success"

@app.route('/simpleedawfs/<string:wfid>')
def get_simple_eda_session(wfid):
    wfs = db_client.get_workflow_session(wfid)
    logger.debug("workflow session from db: %s" % wfs.to_json())


    # data_cols = {col.colIndex: col for col in ds.get_data_columns()}
    logger.debug("*********************************************")
    logger.debug("Data columns: %s" % data_cols)
    all_viz = db_client.get_visualizations(wfs.visualizations)
    logger.debug("*********************************************")
    for viz in all_viz:
        logger.debug("##########################################")
        logger.debug("Viz: %s" % str(viz.as_dict()))
        logger.debug("Adding viz to data col: %s" % str(data_cols[viz.data_attr.colIndex]))
        # logger.debug("Data_col entry to modify: %s" % str(data_cols[viz['data_attr']['colIndex']]))
        # data_cols[viz['data_attr']['colIndex']]['viz_dic'] = viz['viz_doc']
    result = {'WorkflowSession': wfs.__dict__,
              'DatasetId': ds.id,
              'DatasetColumns': [d.to_json() for d in ds.get_data_columns()]
    }
    logger.debug("EDA Session with datasetd and datacols: \n%s" % json.dumps(result))

    return json.dumps(result)


@app.route("/testbokeh1")
def get_bokeh1():
    logger.debug("Testing bokeh 1")
     
    with pull_session(url=bokeh_server_url) as session:
        # update or customize that session
        session.document.roots[0].children[1].title.text = "Special Sliders For A Specific User!"

        # generate a script to load the customized session
        embed_script = server_session(session_id=session.id, url=bokeh_server_url)
        logger.debug("Got script:")
        logger.debug(embed_script)
        embed_url = re.findall(r'src="(.*)" ', embed_script)[0]
        script_id = re.findall(r'id="(.*)"', embed_script)[0]
        logger.debug(embed_url)
        logger.debug(script_id)
        # embed_script = '<script>alert("Testing bokeh flask")</script>'


        # use the script in the rendered page
        # return embed_script
        # return json.dumps({"script_url": embed_url, "script_id": script_id})
        return json.dumps({"script": embed_script})
        # return render_template('embed.html', script=embed_script, framework="Bokeh", template="Flask")


@app.route("/testbokeh2")
def get_bokeh2():
    logger.debug("Testing bokeh 2")
     
    with pull_session(url=bokeh_server_url) as session:
        # update or customize that session
        session.document.roots[0].children[1].title.text = "Special Sliders For A Specific User!"

        # generate a script to load the customized session
        embed_script = server_session(session_id=session.id, url=bokeh_server_url)
        logger.debug("Got script:")
        logger.debug(embed_script)
        embed_url = re.findall(r'src="(.*)" ', embed_script)[0]
        script_id = re.findall(r'id="(.*)"', embed_script)[0]
        logger.debug(embed_url)
        logger.debug(script_id)
        # embed_script = '<script>alert("Testing bokeh flask")</script>'


        # use the script in the rendered page
        # return embed_script
        # return json.dumps({"script_url": embed_url, "script_id": script_id})
        return json.dumps({"script": embed_script})
        # return render_template('embed.html', script=embed_script, framework="Bokeh", template="Flask")


@app.route('/ds/getDataset/<string:dsid>')
def get_dataset(dsid):
    ds = db_client.get_dataset_metadata(dsid)
    logger.debug("dataset json: %s" % (ds.to_json()))
    return ds.to_json()

@app.route('/prob/getProblem/<string:pid>', methods = ['GET', 'PUT'])
def get_problem(pid):
    if request.method == 'GET':
        prob = db_client.get_problem(pid)
        logger.debug("problem json: %s" % (prob.to_json()))
        return prob.to_json()
    if request.method == 'PUT':
        data = json.loads(request.data)
        if '_id' in data.keys():
            logger.debug("removing _id field from data")
            del data['_id']
            logger.debug("data after removing _id: %s" % str(data))
        prob = ProblemDesc.from_json(data)
        result = db_client.replace_problem(pid, prob)
        if result:
            return "Success"
        else:
            return "Error"


@app.route('/ds/getDataCols/<string:dsid>')
def get_data_columns(dsid):
    """
    Return a list of the data columns for each data resource in the dataset

    """
    ds = db_client.get_dataset_metadata(dsid)
    result = {'DatasetId': ds.id,
              'DatasetColumns': [d.to_json() for d in ds.get_data_columns()]
    }

    logger.debug(result)
    # return result
    return json.dumps(result)

@app.route('/test/Hello')
def hello():
    return "Hello World"


@app.route('/test/isReady')
def is_ready():
    """
    Check if ta3 and ta2 systems are ready for testing

    """

    logger.info("Checking if ta2 is ready")

    # Init the server connection
    address = config.get_ta2_addr()
    name = config.get_ta2_name()
    logger.info("using server at address %s" % address)
    serv = TA2Client(address, 
            name=name)
    try:
        reply = serv.hello()
        logger.info(reply)
    except:
        logger.info("TA2 not responding to hello")
        return "False"
    logger.info("Checking Datashop status")
    ta3_status = urllib.request.urlopen("http://" + config.get_tigris_addr()).getcode()
    if ta3_status == 200:
        return "True"
    else:
        return "False"

@app.route('/test/getAllDBDatasets')
def get_db_datasets():
    """
    Get a list of all datasets in the db

    """
    logger.info("Retreiving all datasets in db")
    datasets = db_client.get_all_datasets()
    ds = [d for d in datasets]
    logger.debug("Got datsets frm db: %s" % str(ds))
    return str(ds)

@app.route('/test/getDatasetList')
def get_dataset_list():
    """
    Get the list of all available datasets

    """
    logger.info("Importing List of available datasets")

    ds_root = config.get_dataset_path()

    # Get dummy workflow session 
    session = ImportDatasetSession(user_id="testUser", workflow_id="testWorkflow",
                                   comp_type="DatasetImporter", comp_id="testDatasetImporter")

    logger.info("Scanning dataset root: %s" % ds_root)
    runner = DatasetImporter(db=db_client, session=session)
    datasets = runner.run(ds_root)

    out_dir = os.path.join('/output/test')
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    out_file_path = path.join(out_dir, 'dataset_list.csv')
    logger.info("Writing dataset list of %i datasets to file: %s" % (len(datasets), out_file_path))
    with open(out_file_path, 'w') as out_file:
        out_csv = csv.writer(out_file, delimiter='\t')
        out_csv.writerow(datasets)

    if len(datasets) > 0:
        return "True"
    else:
        return "False"

@app.route('/test/selectDataset')
def select_dataset():
    """
    Get the dataset by name

    """
    logger.info("Importing D3M Dataset selected by user")

    ds_root = config.get_dataset_path()
    name = "acled"
    runner = DatasetSelector()
    ds = runner.run(ds_root, name)

    out_dir = os.path.join('/output/test')
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    out_file_path = path.join(out_dir, 'dataset.json')
    logger.info("Writing dataset json to: %s" % out_file_path)
    ds.to_component_out_file(out_file_path)
    if ds is not None:
        return "True"
    else:
        return "False"
    

@app.route('/test/getDefaultProblem')
def get_default_problem():
    """
    Get default problem associated with the dataset

    """
    logger.info("Generating Problem Statement based on default problem for given dataset")

    out_dir = os.path.join('/output/test')
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
  
    ds_file = path.join(out_dir, 'dataset.json')
    ds = D3MDataset.from_component_out_file(ds_file)
    logger.debug("Dataset json: %s" % str(ds))
    
    runner = DefaultProblemGenerator()
    prob_desc = runner.run(ds)

    out_file_path = path.join(out_dir, 'problem.json')
    logger.info("Writing problem json to: %s" % out_file_path)
    prob_desc.to_file(out_file_path)

    if prob_desc is not None:
        return "True"
    else:
        return "False"
    

@app.route('/test/modelSearch')
def model_search():
    """
    Search and fit models for a given dataset and problem

    """
    logger.info("Running Pipeline Search on TA2")

    out_dir = os.path.join('/output/test')
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
  
    # Open dataset json
    ds_file = path.join(out_dir, 'dataset.json')
    ds = D3MDataset.from_component_out_file(ds_file)
    logger.debug("Dataset json parse: %s" % str(ds))

    # Get the Problem Doc to forulate the Pipeline request
    prob_file = path.join(out_dir, 'problem.json')
    logger.debug("Problem input: %s" % prob_file)
    prob = ProblemDesc.from_file(prob_file)
    logger.debug("Got Problem Description: %s" % prob.print())

    # Init the server connection
    address = config.get_ta2_addr()
    name = config.get_ta2_name()
    logger.info("using server at address %s" % address)
    serv = TA2Client(address, 
            name=name)

    # For Task 1 writing problem discovery output
    out_path = out_dir

    # Run model search
    runner = ModelSearch()
    m_index, models, result_df = runner.run(ds, prob, serv, out_path)

    # Write output of component
    
    # Write model fit id info to output file
    model_out_file_path = path.join(out_dir, 'fit-models.tsv')
    FittedModelSetIO.to_file(model_out_file_path, models, m_index)

    # # Write model predictions to output file
    pred_out_file_path = path.join(out_dir, 'predictions.tsv')
    result_df.to_csv(pred_out_file_path, sep='\t', index=True, header=True)

    logger.debug("Number of models: %i" % len(m_index))
    if len(m_index) > 0:
        return "True"
    else:
        return "False"


@app.route('/test/modelRank')
def model_rank():
    """
    Score the models and rank them accordingly

    """
    logger.info("Running Pipeline Search on TA2")

    out_dir = os.path.join('/output/test')
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
  
    # Open dataset json
    ds_file = path.join(out_dir, 'dataset.json')
    ds = D3MDataset.from_component_out_file(ds_file)
    logger.debug("Dataset json parse: %s" % str(ds))

    # Decode the models from file
    m_file = path.join(out_dir, 'fit_models.tsv')
    logger.debug("Model file input: %s" % m_file)
    m_index, fitted_models, models = FittedModelSetIO.from_file(m_file)

    # Init the server connection
    address = config.get_ta2_addr()
    name = config.get_ta2_name()
    logger.info("using server at address %s" % address)
    serv = TA2Client(address, 
            name=name)

    # Create the metric(s) to use in the score request
    metric = Metric("accuracy")

    ordering = "lower_is_better"

    # Get Ranked list of models
    runner = ModelRanker()
    ranked_models = runner.run(models, m_index, ds, metric, ordering, serv)

    # Write ranked models to file
    out_file_path = path.join(out_dir, "ranked-models.tsv")
    ModelRankSetIO.to_file(out_file_path, ranked_models, m_index)

    if len(ranked_models) == len(m_index):
        return "True"
    else:
        return "False"



@app.route('/test/modelExport')
def model_export():
    """
    Export the list of ranked models

    """
    logger.info("Export set of models for d3m evaluation")

    out_dir = os.path.join('/output/test')
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
  
    # Decode the models from file
    r_model_file = path.join(out_dir, "ranked-models.tsv")
    logger.debug("ModelExport file input: %s" % args.file0)
    m_index, ranked_models = ModelRankSetIO.from_file(args.file0)

    # Init the server connection
    address = config.get_ta2_addr()
    name = config.get_ta2_name()
    logger.info("using server at address %s" % address)
    serv = TA2Client(address, 
            name=name)

    #Create model writer 
    runner = ModelExporter()
    runner.run(config.get_out_path(), ranked_models, serv) 

    # If no exceptions were through, return true
    return "True"


if __name__ == '__main__':
    config = SettingsFactory.get_env_settings()
    dx_config = SettingsFactory.get_dx_settings()
    db_client = DXDB(dx_config.get_db_backend_url())
    bokeh_server_url = "http://" + dx_config.get_viz_server_url() 
    
    if os.environ['VIRTUAL_PORT'] is not None:
        my_port = int(os.environ['VIRTUAL_PORT'])
    else:
        my_port = 8081

    app.run(debug=True,host='0.0.0.0', port=my_port)
