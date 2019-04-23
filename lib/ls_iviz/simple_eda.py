
# Author: Steven C. Dang

# Classes to generate Simple EDA

import logging
import requests
from abc import ABC, abstractmethod

from bokeh.client import pull_session
from bokeh.embed import server_session

logger = logging.getLogger(__name__)

class SimpleEDAViz(ABC):

    def __init__(self, viz_server, eda_session, dataset, resource, data_attr):
        self.viz_server = viz_server
        self.workflow_session = eda_session
        self.dataset = dataset
        self.resoure = resource
        self.data_attr = data_attr

        self.viz_doc = None
        self.viz_type = None

    @abstractmethod
    def generate(self):
        logger.info("Generating simple eda viz")

class SimpleNumericEDAViz(SimpleEDAViz):

    def __init__(self, viz_server, eda_session, dataset, resource, data_attr):
        super().__init__(viz_server, eda_session, dataset, resource, data_attr)
        self.viz_type = "Simple Numeric EDA"

    def generate(self):
        logger.info("Generating Simple Numeric EDA Viz")
        viz_addr = self.viz_server.get_address()

        with pull_session(url=viz_addr) as session:
            # update or customize that session
            doc = session.document
            # generate a script to load the customized session
            embed_script = server_session(session_id=session.id, url=viz_addr)
            logger.debug("Got embed script for viz:\n%s" % str(embed_script))

            self.viz_doc = embed_script


class SimpleCategoricalEDAViz(SimpleEDAViz):

    def __init__(self, viz_server, eda_session, dataset, resource, data_attr):
        super().__init__(viz_server, eda_session, dataset, resource, data_attr)
        self.viz_type = "Simple Categorical EDA"

    def generate(self):
        logger.info("Generating Simple Categorical EDA Viz")
        viz_addr = self.viz_server.get_address()

        with pull_session(url=viz_addr) as session:
            # update or customize that session
            doc = session.document
            # generate a script to load the customized session
            embed_script = server_session(session_id=session.id, url=viz_addr)
            logger.debug("Got embed script for viz:\n%s" % str(embed_script))

            self.viz_doc = embed_script





