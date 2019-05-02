import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { MatButtonModule, MatCheckboxModule } from '@angular/material';

import { Dataset, DatasetIntf, DataAttribute, datasetFromJson } from '../lib/dataset';
import { DataService } from "../lib/data.service";
import { WorkflowSession, SimpleEDASession } from "../lib/workflowSession";

declare let swal: any;

@Component({
  selector: 'app-variable-explorer',
  templateUrl: './variable-explorer.component.html',
  styleUrls: ['./variable-explorer.component.scss']
})
export class VariableExplorerComponent implements OnInit {
  
  dataset: Dataset;
  dataCols: DataAttribute[];
  activeVariable: DataAttribute;
  
  constructor(private http: HttpClient,
              private dataService: DataService,
              private sanitizer: DomSanitizer,
              private route: ActivatedRoute,
              private location: Location
  ) { 
    //this.dataCols = this.dataset.columns;

  }

  ngOnInit() {
    let wfid: string = this.get_session_id();
    this.dataService.getWorkflowSession(wfid).subscribe(result => console.log(result));
    //this.dataService.getWorkflowSession(wfid).subscribe((result: SimpleEDASession) => this.get_data_columns(result));
  }

  get_session_id() {
    // Get the workflow session id using the page route
    const wfid = this.route.snapshot.paramMap.get('wfid');
    console.log("Got workflow Id: ", wfid);
    return wfid

  }

  parse_session_data(sesData: SimpleEDASession) void {

  }

  get_data_columns(wfs: SimpleEDASession): DataAttribute[] {
    // Get the associated dataset data columns using the dataset id from a workflow session
    console.log("Got workflow session: ", wfs);
    console.log("Getting dataset columns using workflow id: ", wfs.dataset_id);
    //this.dataService.getDataset(wfs.dataset_id).subscribe((result: DatasetIntf) => console.log(result)); 
    this.dataService.getDataset(wfs.dataset_id).subscribe((result: DatasetIntf) => this.dataset = datasetFromJson(result)); 
    return [];

  }

  updateVariableView(dt: DataAttribute): void {
    console.log(dt.colName);
    this.activeVariable = dt;
    this.dataService.testBokeh1().subscribe(result => console.log(result));
    //this.dataService.testBokeh().subscribe(result => console.log(result['script_url']));
    //this.dataService.testBokeh().subscribe(result => this.edaView = this.sanitizer.bypassSecurityTrustResourceUrl(result['script_url']));
  }

}
