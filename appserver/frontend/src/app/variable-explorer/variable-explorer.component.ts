import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import {MatButtonModule, MatCheckboxModule} from '@angular/material';

import { Dataset, DatasetIntf, DataAttribute, datasetFromJson } from '../lib/dataset';
import { DataType } from '../lib/dataType';
import { DataService } from "../lib/data.service";

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
              private sanitizer: DomSanitizer) { 
    //this.dataCols = this.dataset.columns;

  }

  ngOnInit() {
    this.dataService.getDataset().subscribe((result: DatasetIntf) => this.dataset = datasetFromJson(result));
  }

  updateVariableView(dt: DataAttribute): void {
    console.log(dt.colName);
    this.activeVariable = dt;
    this.dataService.testBokeh().subscribe(result => console.log(result));
    //this.dataService.testBokeh().subscribe(result => console.log(result['script_url']));
    //this.dataService.testBokeh().subscribe(result => this.edaView = this.sanitizer.bypassSecurityTrustResourceUrl(result['script_url']));
  }

}
