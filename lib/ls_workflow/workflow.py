
# Author: Steven C. Dang

# Class representing an ordered set of operations on a given data input

import logging
import os.path as path
import os
from io import IOBase
import json
import hashlib
from datetime import datetime
import pprint

from ls_dataset.d3m_dataset import D3MDataset

logger = logging.getLogger(__name__)



class ProblemDesc(object):
    """
