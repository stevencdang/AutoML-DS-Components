# Author: Steven C. Dang

# Test all datasets on baseline


import logging

# Workflow component specific imports
from ls_utilities.ls_wf_settings import SettingsFactory
from ls_utilities.cmd_parser import get_default_arg_parser, get_session_info
from ls_utilities.ls_logging import setup_logging
from ls_utilities.ls_wf_settings import *
from dxdb.dx_db import DXDB
from ls_utilities.dexplorer import *
from user_ops.modeling import *
from user_ops.dataset import *
from user_ops.problem import *
from dxdb.workflow_session import *

from ls_problem_desc.ls_problem import ProblemDesc
from ls_problem_desc.d3m_problem import DefaultProblemDesc
from d3m_ta2.ta2_client import TA2Client
from d3m_eval.summer_2018.prob_discovery import ProblemDiscoveryWriter
from modeling.models import *
from modeling.component_out import *
from ls_utilities.html import IframeBuilder


__version__ = '0.1'


if __name__ == '__main__':
    # Parse argumennts
    parser = get_default_arg_parser("Test baseline components")
    args = parser.parse_args()

    if args.is_test is not None:
        is_test = args.is_test == 1
    else:
        is_test = False

    # Get config file
    config = SettingsFactory.get_settings(path.join(args.programDir, 'program', 'settings.cfg'), 
                                          program_dir=args.programDir,
                                          working_dir=args.workingDir,
                                          is_test=is_test
                                          )
    # Get config for dx services
    dx_config = SettingsFactory.get_dx_settings()


    # Setup Logging
    setup_logging(config)
    logger = logging.getLogger('baseline_tester')

    ### Begin Script ###
    logger.info("Running Script to test TA3TA2 baseline over all datasets")

    # Get connection to db
    logger.debug("DB URL: %s" % dx_config.get_db_backend_url())
    db = DXDB(dx_config.get_db_backend_url())

    # get Connection to Dexplorer Service
    dex = DexplorerUIServer(dx_config.get_dexplorer_url())

    # Create false metadata for workflow sessions
    user_id = "Baseline Test User"
    workflow_id = "baseline1"

    # Create workflow session for Dataset Import
    comp_type = "DatasetImporter"
    comp_id = "DatasetImporter-1-x12345"

    session = ImportDatasetSession(user_id=user_id, workflow_id=workflow_id, 
                                   comp_type=comp_type, comp_id=comp_id)
    session = db.add_workflow_session(session)
    logger.debug("Created new Dataset Import Session: %s" % session.to_json())

    # Read in the dataset json
    ds_root = config.get_dataset_path()
    runner = DatasetImporter(db, session)
    datasets = runner.run(ds_root)

    for dsid in datasets:
        
        ds = db.get_dataset_metadata(dsid)

        logger.info("*******************************************")
        logger.info("Testing with dataset: %s" % ds.name)
        logger.info("*******************************************")


        # Grabbing default problem
        comp_type = "ProblemCreator"
        comp_id = comp_type + "-1-x12345"

        # Initialize new session
        prob_session = ProblemCreatorSession(user_id=user_id, workflow_id=workflow_id, 
                                       comp_type=comp_type, comp_id=comp_id)
        prob_session.set_dataset_id(ds._id)

        runner = DefaultProblemGenerator()
        def_prob = runner.run(ds)
        def_prob._id = db.insert_problem(def_prob)
        prob_session.prob_id = def_prob._id
        prob_session.add_suggestion_prob(def_prob)
        prob_session.set_state_complete()
        prob_session = db.add_workflow_session(prob_session)

        # Initialize model search session
        comp_type = "ModelSearch"
        comp_id = comp_type + "-1-x12345"

        # Initialize new session
        search_session = ModelSearchSession(user_id=user_id, workflow_id=workflow_id, 
                                       comp_type=comp_type, comp_id=comp_id)
        search_session.set_dataset_id(ds._id)
        search_session.set_problem_id(def_prob._id)
        search_session.set_input_wfids([prob_session._id])

        # Init the TA2 server connection
        address = config.get_ta2_url()
        name = config.get_ta2_name()
        
        logger.info("using server at address %s" % address)
        if is_test:
            serv = TA2Client(address, debug=True, out_dir=args.workingDir, 
                    name=name)
        else:
            serv = TA2Client(address, 
                    name=name)
        search_session.ta2_addr = address
        search_session = db.add_workflow_session(search_session)

        runner = ModelSearch(db, search_session, serv)
        # m_index, models, result_df, score_data, ranked_models = runner.run(ds, prob, out_path)
        runner.run(ds, def_prob)
        search_session = runner.sess

        ranked_models = []
        for rm_id in search_session.ranked_mdl_ids:
            rm = RankedModel.from_json(db.get_object('ranked_models', rm_id))
            logger.debug("Got ranked model from db to export: %s" % str(rm))
            ranked_models.append(rm)

        runner = ModelExporter()
        runner.run(config.get_out_path(), ranked_models, serv) 

        serv.end_search_solutions(search_session.search_id)
        logger.info("Ended search solution after exporting: %s" % search_session.search_id)
