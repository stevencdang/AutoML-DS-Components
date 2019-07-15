import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

import { Dataset, DatasetResource } from "../lib/dataset";
import { DataService } from "../lib/data.service";
import { WorkflowSession, DatasetImporterSession } from "../lib/workflowSession";


@Component({
  selector: 'app-dataset-importer',
  templateUrl: './dataset-importer.component.html',
  styleUrls: ['./dataset-importer.component.scss']
})
export class DatasetImporterComponent implements OnInit {

  wfs: DatasetImporterSession;
  available_datasets: Dataset[];
  selected_dataset: Dataset;
  selected_resource: DatasetResource;

  constructor(private http: HttpClient,
              private dataService: DataService,
              private sanitizer: DomSanitizer,
              private route: ActivatedRoute,
              private location: Location
  ) { 
    
  }

  ngOnInit() {
    let wfid: string = this.get_session_id();
    this.dataService.getWorkflowSession(wfid).subscribe((result: DatasetImporterSession) => this.parse_session_data(result));
    this.available_datasets = [];
    
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

  get_session_id() {
    // Get the workflow session id using the page route
    const wfid = this.route.snapshot.paramMap.get('wfid');
    console.log("Got workflow Id: ", wfid);
    return wfid;
  }

  parse_session_data(sesData: DatasetImporterSession) {
    console.log("Parsing session data");
    console.log(sesData);
    this.wfs = sesData;
    for (var dsid of this.wfs.available_datasets) {
      console.log("Dataset id to retrieve: ", this.wfs.available_datasets[dsid]);
      if (this.wfs.dataset_id != undefined) {
        console.log("Current session dataset slected: %s", this.wfs.dataset_id)
        if (this.wfs.dataset_id == dsid) {
          console.log("*************************************");
          console.log("*************************************");
          console.log("*************************************");
          console.log("*************************************");
          console.log("dataset already selected. setting to state variable");
          this.dataService.getDataset(this.wfs.available_datasets[dsid]).subscribe(result => this.parse_new_dataset(result, true));
        } else {
          console.log("****************2*********************");
          console.log("*****************2********************");
          console.log("****************2*********************");
          console.log("*****************2********************");
          this.dataService.getDataset(this.wfs.available_datasets[dsid]).subscribe(result => this.parse_new_dataset(result, false));
        }
      } else {
          console.log("****************3*********************");
          console.log("*****************3********************");
          console.log("****************3*********************");
          console.log("*****************3********************");
        this.dataService.getDataset(this.wfs.available_datasets[dsid]).subscribe(result => this.parse_new_dataset(result, false));
      }
    }
  }

  parse_new_dataset(ds: Dataset, setSelected: Boolean) {
    console.log("Got dataset: ", ds.about.datasetID);
    this.available_datasets.push(ds);
    if (setSelected) {
      this.selected_dataset = ds;
    }
  }

  isSelectedDataset(ds: Dataset) {
    if (this.selected_dataset === undefined) {
      return false;
    } else {
      return ds._id == this.selected_dataset._id;
    }
  }

  onSelectDataset(ds: Dataset) {
    console.log("Selected dataset: ", ds);
    if (this.selected_dataset != undefined) {
      if (this.selected_dataset._id == ds._id) {
        this.selected_dataset = undefined;
      } else {
        this.selected_dataset = ds;
      }
    } else {
      this.selected_dataset = ds;
    }

  }

  onSelectResource(res: DatasetResource) {
    console.log("Selected Resource: ", res);
    this.selected_resource=res;
  }

  importDataset() {
    console.log("Importing Selected dataset: ", this.selected_dataset);
    this.wfs.dataset_id = this.selected_dataset._id;
    this.wfs.state = "Dataset Imported"
    let updates: Object = {state: this.wfs.state, dataset_id: this.wfs.dataset_id};
    this.dataService.updateWorkflowSession(this.wfs._id, updates).subscribe(result => console.log(result));
  }

}
