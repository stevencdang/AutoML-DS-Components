# from flask import Flask
import logging
from logging.config import dictConfig
from flask import Flask, render_template, url_for
import flask.logging
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
import re
import sys

from ls_utilities.ls_logging import setup_logging
from ls_utilities.ls_wf_settings import *
from ls_dataset.d3m_dataset import D3MDataset
from dxdb.dx_db import DXDB
from dxdb.workflow_session import *

from bokeh.client import pull_session
from bokeh.embed import server_session

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

@app.route('/wfs/<string:wfid>')
def get_simple_eda_session(wfid):
    wfs = db_client.get_workflow_session(wfid)
    # logger.debug("workflow session from db: %s" % db_wfs)
    # wfs = SimpleEDASession.from_json(db_wfs)
    # logger.debug("workflow session to json: %s" % json.dumps(wfs.__dict__))
    ds = db_client.get_dataset_metadata(wfs.dataset_id)
    data_cols = {col.colIndex: col.to_json() for col in ds.get_data_columns()}

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


@app.route('/ds/getDataset')
def get_dataset():

    ds = db_client.get_dataset_metadata()
    logger.debug([str(d) for d in ds.get_data_columns()])
    # return json.dumps({"result": "Hello World"})
    return ds.to_json()

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


if __name__ == '__main__':
    db_client = DXDB('localhost:27017')
    config = Settings("src/settings.cfg")
    bokeh_server_url = "http://sophia.stevencdang.com:5100/test"

    app.run(debug=True,host='0.0.0.0')
