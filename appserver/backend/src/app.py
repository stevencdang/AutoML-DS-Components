# from flask import Flask
import logging
from flask import Flask, render_template, url_for
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
import re

from ls_dataset.d3m_dataset import D3MDataset
from dxdb.dx_db import DXDB
from dxdb.workflow_session import *

from bokeh.client import pull_session
from bokeh.embed import server_session


app = Flask(__name__)
CORS(app)
db_client = DXDB('localhost:27017')

bokeh_server_url = "http://sophia.stevencdang.com:5100/test"



@app.route('/')
def main():
    return "Hello World"

@app.route('/wfs/<string:wfid>')
def get_simple_eda_session(wfid):
    db_wfs = db_client.get_workflow_session(wfid)
    app.logger.debug("workflow session from db: %s" % db_wfs)
    wfs = SimpleEDASession.from_json(db_wfs)
    app.logger.debug("workflow session to json: %s" % json.dumps(wfs.__dict__))
    return json.dumps(wfs.__dict__)
      


@app.route("/testbokeh1")
def get_bokeh1():
    app.logger.debug("Testing bokeh 1")
     
    with pull_session(url=bokeh_server_url) as session:
        # update or customize that session
        session.document.roots[0].children[1].title.text = "Special Sliders For A Specific User!"

        # generate a script to load the customized session
        embed_script = server_session(session_id=session.id, url=bokeh_server_url)
        app.logger.debug("Got script:")
        app.logger.debug(embed_script)
        embed_url = re.findall(r'src="(.*)" ', embed_script)[0]
        script_id = re.findall(r'id="(.*)"', embed_script)[0]
        app.logger.debug(embed_url)
        app.logger.debug(script_id)
        # embed_script = '<script>alert("Testing bokeh flask")</script>'


        # use the script in the rendered page
        # return embed_script
        # return json.dumps({"script_url": embed_url, "script_id": script_id})
        return json.dumps({"script": embed_script})
        # return render_template('embed.html', script=embed_script, framework="Bokeh", template="Flask")


@app.route("/testbokeh2")
def get_bokeh2():
    app.logger.debug("Testing bokeh 2")
     
    with pull_session(url=bokeh_server_url) as session:
        # update or customize that session
        session.document.roots[0].children[1].title.text = "Special Sliders For A Specific User!"

        # generate a script to load the customized session
        embed_script = server_session(session_id=session.id, url=bokeh_server_url)
        app.logger.debug("Got script:")
        app.logger.debug(embed_script)
        embed_url = re.findall(r'src="(.*)" ', embed_script)[0]
        script_id = re.findall(r'id="(.*)"', embed_script)[0]
        app.logger.debug(embed_url)
        app.logger.debug(script_id)
        # embed_script = '<script>alert("Testing bokeh flask")</script>'


        # use the script in the rendered page
        # return embed_script
        # return json.dumps({"script_url": embed_url, "script_id": script_id})
        return json.dumps({"script": embed_script})
        # return render_template('embed.html', script=embed_script, framework="Bokeh", template="Flask")


@app.route('/ds/getDataset')
def get_dataset():

    ds = db_client.get_dataset_metadata()
    app.logger.debug([str(d) for d in ds.get_data_columns()])
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

    app.logger.debug(result)
    # return result
    return json.dumps(result)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
