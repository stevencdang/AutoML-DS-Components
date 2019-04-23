
# Author: Steven C. Dang

# Classes to generate Simple EDA

import logging
import requests
from abc import ABC, abstractmethod

from bokeh.client import pull_session
from bokeh.plotting import figure
from bokeh.embed import server_session

logger = logging.getLogger(__name__)

class SimpleEDAViz(ABC):

    def __init__(self, viz_server, eda_session, dataset, resource, data_attr):
        self.viz_server = viz_server
        self.workflow_session = eda_session
        self.dataset = dataset
        self.resource = resource
        self.data_attr = data_attr
        
        self._id = None
        self.viz_doc = None
        self.viz_type = None

    @abstractmethod
    def generate(self):
        logger.info("Generating simple eda viz")

    def to_json(self):
        out = {
                'viz_server': self.viz_server.get_address(),
                'workflow_session': self.workflow_session.__dict__,
                'dataset': self.dataset._id,
                'resource': self.resource.resID,
                'data_attr': self.data_attr.to_json(),
                'viz_doc': str(self.viz_doc),
        }
        if self._id is not None:
            out['_id'] = str(self._id),
        if self.viz_type is not None:
            out['viz_type']  = self.viz_type
        return out


class SimpleNumericEDAViz(SimpleEDAViz):

    def __init__(self, viz_server, eda_session, dataset, resource, data_attr):
        super().__init__(viz_server, eda_session, dataset, resource, data_attr)
        self.viz_type = "Simple Numeric EDA"

    def generate(self):
        logger.info("Generating Simple Numeric EDA Viz")
        viz_addr = self.viz_server.get_address()
        logger.debug("Connecting to server at address: %s" % viz_addr)

        with pull_session(url=viz_addr) as session:
            # update or customize that session
            doc = session.document

            p = figure(plot_width=400, plot_height=400)

            # add a circle renderer with a size, color, and alpha
            p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)

            doc.add_root(p)
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
        logger.debug("Connecting to server at address: %s" % viz_addr)

        with pull_session(url=viz_addr) as session:
            # update or customize that session
            doc = session.document

            p = figure(plot_width=400, plot_height=400)

            # add a square renderer with a size, color, and alpha
            p.square([5, 4, 3, 2, 1], [6, 7, 2, 4, 5], size=20, color="olive", alpha=0.5)
            
            doc.add_root(p)
            # generate a script to load the customized session
            embed_script = server_session(session_id=session.id, url=viz_addr)
            logger.debug("Got embed script for viz:\n%s" % str(embed_script))

            self.viz_doc = embed_script

