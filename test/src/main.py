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

test_data_names = ['DA_college_debt',
                   'DA_medical_malpractice',
                   'DA_ny_taxi_demand',
                   'DA_poverty_estimation',
                   'LL0_acled_reduced',
                   'LL1_336_MS_Geolife_transport_mode_prediction',
                   'LL1_336_MS_Geolife_transport_mode_prediction_separate_lat_lon',
                   'LL1_736_population_spawn',
                   'LL1_736_population_spawn_simpler',
                   'LL1_penn_fudan_pedestrian',
                   'LL1_VTXC_1343_cora',
                   'LL1_VTXC_1369_synthetic',
                   'SEMI_1040_sylva_prior',
                   'SEMI_1044_eye_movements',
                   'SEMI_1053_jm1',
                   'SEMI_1217_click_prediction_small',
                   'SEMI_1459_artificial_characters',
                   'SEMI_155_pokerhand',
                   'SUPDATA_usps_digit_classification'
                   ]
                   



if __name__ == '__main__':
    # Setup paths to manage output directories
    out_dir = "/output"
    main_out_dir = os.path.join(out_dir, "pipelines_ranked")

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
    
    logger.info("Dataset names to compare: %s" % test_data_names)
    for dsid in datasets:
        
        ds = db.get_dataset_metadata(dsid)

        # ds_name = ds.name.lower().replace("_", " ")
        # logger.info("Checking if %s is in list of datasets: %r" % (ds_name, ds_name in ds_names))
        # logger.info("Cfolder folder folder folder folder folder folder hecking if folder %s is in list of datasets: %r" % (ds.dpath, any(dpath in ds.dpath for dpath in test_data_names)))
            # logger.info("*******************************************")
            # logger.info(ds_names[0])
            # logger.info(ds_name)
            # logger.info(ds_names[1])
            # logger.info(ds_names[0] == 'da college debt')
            # logger.info(ds_name == ds_names[0])
            # logger.info(ds_name in ds_names)
            # logger.info("da college debt in list: %r" % 'da college debt' in ds_names)
            # logger.info("*******************************************")
        if any(dpath in ds.dpath for dpath in test_data_names):

            logger.info("*******************************************")
            logger.info("Testing with dataset: %s" % ds.name)
            logger.info("*******************************************")

            # Write dataset to file in output
            ds_name = os.path.split(ds.dpath)[1]
            out_path = os.path.join(out_dir, ds_name)
            os.mkdir(out_path)
            out_file = os.path.join(out_path, "dataset.json")
            ds.to_json(out_file)


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

            # Move exported files to dataset directory
            for f in os.listdir(main_out_dir):
                if not os.path.isdir(os.path.join(main_out_dir, f)):
                    logger.debug("Moving %s to %s" % (os.path.join(main_out_dir, f),
                                    os.path.join(out_path, f)))
                    try: 
                        os.rename(os.path.join(main_out_dir, f), os.path.join(out_path, f))
                    except Exception as e:
                        logger.error("Ran into error when moving pipeline file: %s" % str(e))


