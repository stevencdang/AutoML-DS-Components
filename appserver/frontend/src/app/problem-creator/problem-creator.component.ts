import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

import { Dataset, DatasetResource } from "../lib/dataset";
import { DataService } from "../lib/data.service";
import { WorkflowSession, ProblemCreatorSession } from "../lib/workflowSession";

@Component({
  selector: 'app-problem-creator',
  templateUrl: './problem-creator.component.html',
  styleUrls: ['./problem-creator.component.scss']
})
export class ProblemCreatorComponent implements OnInit {

  wfs: ProblemCreatorSession;

  constructor(private http: HttpClient,
              private dataService: DataService,
              private sanitizer: DomSanitizer,
              private route: ActivatedRoute,
              private location: Location
  ) { 
    
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
    this.wfs = sesData;
    //for (let dsid in this.wfs.available_datasets) {
      //if (this.wfs.dataset_id != undefined) {
        //if (this.wfs.dataset_id == dsid) {
          //console.log("dataset already selected. setting to state variable");
          //this.dataService.getDataset(this.wfs.available_datasets[dsid]).subscribe(result => this.parse_new_dataset(result, true));
        //} else {
          //this.dataService.getDataset(this.wfs.available_datasets[dsid]).subscribe(result => this.parse_new_dataset(result, false));
        //}
      //} else {
        //this.dataService.getDataset(this.wfs.available_datasets[dsid]).subscribe(result => this.parse_new_dataset(result, false));
      //}
    //}
  }

}
