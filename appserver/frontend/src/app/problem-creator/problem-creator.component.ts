import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

import {SelectItem} from 'primeng/api';

import { Dataset, DatasetResource } from "../lib/dataset";
import { Problem, ProblemInput, ProblemTarget, PerformanceMetric } from "../lib/problem";
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
  problem_target: string;
  possible_targets: ProblemInput[];
  problem_metric: string;
  suggest_probs: Problem[];
  //UI options
  problem_targets: SelectItem[];
  task_types: SelectItem[];
  task_subtypes: SelectItem[];
  problem_metrics: SelectItem[];

  constructor(private http: HttpClient,
              private dataService: DataService,
              private sanitizer: DomSanitizer,
              private route: ActivatedRoute,
              private location: Location
  ) { 
    this.task_types = [
      {label: "classification", value: "classification"},
      {label: "regression", value: "regression"},
      {label: "clustering", value: "clustering"},
      {label: "link prediction", value: "link prediction"},
      {label: "vertex nomination", value: "vertex nomination"},
      {label: "vertex classification", value: "vertex classification"},
      {label: "community detection", value: "community detection"},
      {label: "graph matching", value: "graph matching"},
      {label: "time series forecasting", value: "time series forecasting"},
      {label: "collaborative filtering", value: "collaborative filtering"},
      {label: "object detection", value: "object detection"},
      {label: "semisupervised classification", value: "semisupervised classification"},
      {label: "semisupervised regression", value: "semisupervised regression"}
    ];
    this.task_subtypes = [
      {label: "binary", value: "binary"},
      {label: "multiclass", value: "multiclass"},
      {label: "multilabel", value: "multilabel"},
      {label: "univariate", value: "univariate"},
      {label: "multivariate", value: "multivariate"},
      {label: "overlapping", value: "overlapping"},
      {label: "nonoverlapping", value: "nonoverlapping"}
    ];
    this.problem_metrics = [
      {label: "accuracy", value: "accuracy"},
      {label: "precision", value:  "precision"},
      {label: "recall", value:  "recall"},
      {label: "f1", value:  "f1"},
      {label: "f1 micro", value:  "f1micro"},
      {label: "f1 macro", value:  "f1macro"},
      {label: "roc auc", value:  "rocauc"},
      {label: "roc auc macro", value:  "rocaucmacro"},
      {label: "roc auc micro", value:  "rocaucmicro"},
      {label: "mean squared error", value:  "meansquarederror"},
      {label: "root mean squared error", value:  "rootmeansquarederror"},
      {label: "mean absolute error", value:  "meanabsoluteerror"},
      {label: "rsquared", value:  "rsquared"},
      {label: "normalized mutual information", value:  "normalizedmutualinformation"},
      {label: "jaccard similarity score", value:  "jaccardsimilarityscore"},
      {label: "precision at top k", value:  "precisionattopk"},
      {label: "object detection ap", value:  "objectdetectionap"},
      {label: "hamming loss", value:  "hammingloss"},
      {label: "average mean reciprocal rank", value:  "averagemeanreciprocalrank"}
    ];
    this.problem_targets = [];
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
            let target: ProblemTarget = new ProblemTarget(
                res.resID,
                col.colIndex,
                col.colName,
                0
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
        this.possible_targets = targets;
        // Turn Problem inputs into select items for ui
        for (let target of targets) {
          let t_name: string = target.targets[0].column_name;
          console.log("Processing column target: ", t_name);
          this.problem_targets.push({label: t_name, value: t_name});
          //let item: SelectItem = new SelectItem(target.targets[0].column_name, target.targets[0].column_name);
          //this.problem_targets.push(item);
        }
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
    this.set_new_problem(prob);
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




  set_problem_target() {
    console.log("state of problem_target", this.problem_target);
    console.log("state of problem", this.problem);
    this.match_target(this.problem_target);
    console.log("set Problem target of problem: ", this.problem);
  }

  set_problem_metric() {
    //this.problem.metrics = [this.problem_metric];
    this.problem.metrics = [new PerformanceMetric(this.problem_metric)];
    console.log("set Problem Metric of problem: ", this.problem);
  }

  copyObject<T> (object:T): T {
        var objectCopy = <T>{};

        for (var key in object)
          {
                    if (object.hasOwnProperty(key))
                      {
                                    objectCopy[key] = object[key];
                                }
                }

        return objectCopy;
  }

  clean_problem(prob: Problem) {
    console.log("Original problem before cleaning fields", prob);
    // COnvert task type to lowercase with spaces
    let task_type: string = prob.task_type.toLowerCase();
    console.log("new task type:", task_type);
    prob.task_type = task_type;
    // Convert subtask type to lowercase

    if (prob.subtype != undefined) {
      let task_subtype: string = prob.subtype.toLowerCase();
      task_subtype.split("_").join(" ");
      console.log("new taks subtype:", task_subtype);
      prob.subtype = task_subtype;

    }
    //Convert metric to metric with lowercase and spaces
    let new_metrics: PerformanceMetric[] = [];
    for (let pmetric of prob.metrics) {
      let metric: string = pmetric.metric;
      console.log("Previous metric:", metric);
      metric = metric.toLowerCase();
      console.log("Lowercase metric:", metric.toLowerCase());
      metric = metric.split("_").join(""); 
      console.log("removed underscores", metric);
      pmetric.metric = metric;
      new_metrics.push(pmetric);
    }
    prob.metrics = new_metrics;
    return prob;
  }


  match_metric(metric: PerformanceMetric) {
    console.log("Matching metric: ", metric);
    for (let m of this.problem_metrics) {
      console.log("checking for match with: ", m);
      if (metric.metric == m.value) {
        console.log("Matched performance metric:", metric, "to label: ", m);
        return m
      }

    }

  }

  match_target(target: string) {
    if (this.possible_targets.length == 0) {
      this.problem_target = t.targets[0].column_name
    } else {
      for (let t of this.possible_targets) {
        console.log("checking for match of, ", target, "with possible target:", t);
        if (target == t.targets[0].column_name) {
          console.log("Found matching target");
          this.problem_target = target;
          return
        }
      }
    }
  }

  set_new_problem(prob: Problem) {
    let new_prob: Problem = this.clean_problem(this.copyObject<Problem>(prob));
    if (this.problem != undefined) {
      let old_id: string = this.problem._id;
      this.problem = new_prob;
      this.problem._id = old_id;
    } else {
      this.problem = new_prob;
    }

    // Set the performance metric state according to that in the problem
    this.problem_metric = new_prob.metrics[0].metric
    // Set the target according to that reflected in the problem
    this.match_target(new_prob.inputs[0].targets[0].column_name);
  }

  use_suggest_prob() {
    console.log("Problem Suggestion Requested", this.suggest_probs[0]);
    console.log("current problem: ", this.problem);
    console.log("Suggested Problem: ", this.suggest_probs[0]);
    this.set_new_problem(this.suggest_probs[0]);

    console.log("Updated problem: ", this.problem);
    console.log("Suggested Problem: ", this.suggest_probs[0]);
  }

  set_problem() {
    console.log("Updating problem in db with current ui state");
    this.dataService.updateProblem(this.problem).subscribe(result => console.log("Result of update problem to db:", result));
    this.wfs.state = "Problem Creation Completed";
    let updates: Object = {state: this.wfs.state};
    this.dataService.updateWorkflowSession(this.wfs._id, updates).subscribe(result => console.log(result));
  }



}

