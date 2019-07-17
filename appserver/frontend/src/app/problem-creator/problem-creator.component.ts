import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

import {SelectItem} from 'primeng/api';

import { Dataset, DatasetResource } from "../lib/dataset";
import { Problem, ProblemTaskTypes, ProblemTaskSubtypes, ProblemInput, ProblemTarget } from "../lib/problem";
import { DataService } from "../lib/data.service";
import { WorkflowSession, DatasetImporterSession, ProblemCreatorSession } from "../lib/workflowSession";

@Component({
  selector: 'app-problem-creator',
  templateUrl: './problem-creator.component.html',
  styleUrls: ['./problem-creator.component.scss']
})
export class ProblemCreatorComponent implements OnInit {

  wfs: ProblemCreatorSession;
  dataset: Dataset;
  input_wfs: DatasetImporterSession[];
  problem: Problem;
  task_type: string;
  suggest_probs: Problem[];
  //UI options
  problem_targets: ProblemInput[];
  task_types: SelectItem[];
  task_subtypes: SelectItem[];
  task_metrics: SelectItem[];

  constructor(private http: HttpClient,
              private dataService: DataService,
              private sanitizer: DomSanitizer,
              private route: ActivatedRoute,
              private location: Location
  ) { 
    this.task_types = [
      {label: "CLASSIFICATION", value: "CLASSIFICATION"},
      {label: "REGRESSION", value: "REGRESSION"},
      {label: "CLUSTERING", value: "CLUSTERING"},
      {label: "LINK_PREDICTION", value: "LINK_PREDICTION"},
      {label: "VERTEX_NOMINATION", value: "VERTEX_NOMINATION"},
      {label: "VERTEX_CLASSIFICATION", value: "VERTEX_CLASSIFICATION"},
      {label: "COMMUNITY_DETECTION", value: "COMMUNITY_DETECTION"},
      {label: "GRAPH_MATCHING", value: "GRAPH_MATCHING"},
      {label: "TIME_SERIES_FORECASTING", value: "TIME_SERIES_FORECASTING"},
      {label: "COLLABORATIVE_FILTERING", value: "COLLABORATIVE_FILTERING"},
      {label: "OBJECT_DETECTION", value: "OBJECT_DETECTION"},
      {label: "SEMISUPERVISED_CLASSIFICATION", value: "SEMISUPERVISED_CLASSIFICATION"},
      {label: "SEMISUPERVISED_REGRESSION", value: "SEMISUPERVISED_REGRESSION"}
    ];
    this.task_subtypes = [
      {label: "BINARY", value: "BINARY"},
      {label: "MULTICLASS", value: "MULTICLASS"},
      {label: "MULTILABEL", value: "MULTILABEL"},
      {label: "UNIVARIATE", value: "UNIVARIATE"},
      {label: "MULTIVARIATE", value: "MULTIVARIATE"},
      {label: "OVERLAPPING", value: "OVERLAPPING"},
      {label: "NONOVERLAPPING", value: "NONOVERLAPPING"}
    ];
  }


  ngOnInit() {
    let wfid: string = this.get_session_id();
    this.dataService.getWorkflowSession(wfid).subscribe((result: ProblemCreatorSession) => this.parse_session_data(result));
    
  }

  get_session_id() {
    // Get the workflow session id using the page route
    const wfid = this.route.snapshot.paramMap.get('wfid');
    console.log("Got workflow Id: ", wfid);
    return wfid;
  }

  is_ready() {
    //Validate that state variables are defined and state is not "not ready" state 
    if (this.wfs === undefined) {
      return false;
    } else {
      return true;
      //if (this.wfs.state == "Not Ready") {
        //return false;
      //} else {
        //return true;
      //}
    }

  }

  parse_session_data(sesData: ProblemCreatorSession) {
    console.log("Parsing session data");
    console.log(sesData);
    // get input workflow and check if inputs have changed
    for (let wfid of sesData.input_wfids) {
      console.log("getting workflow_ids")
      this.dataService.getWorkflowSession(wfid).subscribe((result: DatasetImporterSession) => this.check_input_wfs(result, sesData));
    }
  }

  check_input_wfs(wfs: DatasetImporterSession, 
    curr_wfs: ProblemCreatorSession) 
  {
    console.log("Adding session to input wfs");
    // Initialize input_wfs if not already
    if (this.input_wfs === undefined) {
      this.input_wfs = [];
    }
    this.input_wfs.push(wfs)
    // If all wfs received, then check change conditions
    if (this.input_wfs.length == curr_wfs.input_wfids.length) {
      console.log("All input workflow ids have been received");
      let is_changed = false;
      for (let iwfs of this.input_wfs) {
        // only datasetimporter sessions are inputs
        console.log(iwfs);
        console.log(iwfs instanceof DatasetImporterSession);
        console.log(iwfs instanceof WorkflowSession);
        console.log("Checking dataset id ", iwfs.dataset_id, 
          "if different from dataset id from workflow session: ", 
          curr_wfs.dataset_id);
        if (iwfs.dataset_id != curr_wfs.dataset_id) {
          console.log("Dataset is changed!");
          is_changed = true;
        }

      }
      if (is_changed) {
        console.log("Input dataset changed, need to reinitialize a problem for this session");
      } else {
        this.wfs = curr_wfs;
        this.init_session();
      }
    }
  }
  process_dataset(ds: Dataset) {
    this.dataset = ds;
    console.log("Got dataset: ", ds);
    let targets: ProblemInput[] = [];
    for (let res of ds.dataResources) {
      console.log("Processing dataset resource for possible targets: ", res);
      let dsid: string = ds._id;
      if (res.isCollection == false && res.resType == "table") {

        for (let col of res.columns) {
          if (col.colName != "d3mIndex") {
            console.log("Adding Problem input for dataset resource column: ", col);
            let target: ProblemTarget = new ProblemTarget(0,
                res.resID,
                col.colIndex,
                col.colName
            );
            console.log("created problem target: ", target);
            let pinpt: ProblemInput = new ProblemInput(dsid, 
              [target],
              []
            );
            console.log("Created new ProblemInput: ", pinpt);
            targets.push(pinpt);
            console.log("Pushed iput to list:", targets);
          }
        }
        this.problem_targets = targets;
      } else {
        console.log("skipping resource, because it is not a table with data to select prediction");
      }
    }
    
  }

  init_session() {
    console.log("Initializing Problem Creator Session with Data");
    //Get Dataset for this workflow
    //this.dataService.getDataset(this.wfs.dataset_id).subscribe((result: Dataset) => this.dataset = result);
    this.dataService.getDataset(this.wfs.dataset_id).subscribe((result: Dataset) => this.process_dataset(result));

    // Get problem for this workflow
    if (this.wfs.prob_id != undefined) {
      this.dataService.getProblem(this.wfs.prob_id).subscribe((result: Problem) => this.init_problem_fields(result));
    }
    // Get the list of problems
    this.suggest_probs = []
    console.log("wfs", this.wfs);
    console.log("Suggested problems: ", this.wfs.suggest_pids.length);
    for (let pid of this.wfs.suggest_pids) {
      this.dataService.getProblem(pid).subscribe((result: Problem) => this.suggest_probs.push(result));
    }


  }

  init_problem_fields(prob: Problem) {
    this.problem = prob;
    console.log("Initializing all relevant field of problem: ", this.problem);
    if (this.problem.name === undefined) {
      this.problem.name = ""
    }
    if (this.problem.description === undefined) {
      this.problem.description = ""
    }
    if (this.problem.task_type ===undefined) {
      this.problem.task_type = ""
    }
    if (this.problem.subtype === undefined) {
      this.problem.subtype = ""
    }
    console.log("Initialized all relevant problem fields: ", this.problem);

  }




  set_problem() {
    console.log("Updating problem in db with current ui state");
  }

  set_problem_target() {
    this.problem.inputs = [this.problem_target];
    console.log("set Problem target of problem: ", this.problem);
  }

  use_suggest_prob() {
    console.log("Problem Suggestion Requested");
  }

}

