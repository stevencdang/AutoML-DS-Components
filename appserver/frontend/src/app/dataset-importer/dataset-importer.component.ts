import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

import { DataService } from "../lib/data.service";
import { WorkflowSession, DatasetImporterSession } from "../lib/workflowSession";

@Component({
  selector: 'app-dataset-importer',
  templateUrl: './dataset-importer.component.html',
  styleUrls: ['./dataset-importer.component.scss']
})
export class DatasetImporterComponent implements OnInit {

  wfs: DatasetImporterSession;

  constructor(private http: HttpClient,
              private dataService: DataService,
              private sanitizer: DomSanitizer,
              private route: ActivatedRoute,
              private location: Location
  ) { 
    
  }

  ngOnInit() {
    let wfid: string = this.get_session_id();
    this.dataService.getWorkflowSession(wfid).subscribe(result => this.parse_session_data(result));
  }

  is_ready() {
    //Validate that state variables are defined and state is not "not ready" state 
    if (this.wfs === undefined) {
      return false;
    } else {
      if (this.wfs.state == "Not Ready") {
        return false;
      } else {
        return true;
      }
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
  }


}
