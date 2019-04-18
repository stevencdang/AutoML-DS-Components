import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {MatButtonModule, MatCheckboxModule} from '@angular/material';
import { Dataset, DatasetIntf, DataAttribute, datasetFromJson } from '../lib/dataset';
import { DataType } from '../lib/dataType';
import { DataService } from "../lib/data.service";

@Component({
  selector: 'app-variable-explorer',
  templateUrl: './variable-explorer.component.html',
  styleUrls: ['./variable-explorer.component.scss']
})
export class VariableExplorerComponent implements OnInit {
  
  dataset: Dataset;
  dataCols: DataType[];
  activeVariable: DataType;
  

  constructor(private http: HttpClient,
              private dataService: DataService) { 
    //this.dataCols = this.dataset.columns;

  }

  ngOnInit() {
    this.dataService.getDataset().subscribe((result: DatasetIntf) => this.dataset = datasetFromJson(result));
  }

  updateVariableView(dt: DataAttribute): void {
    console.log(dt.colName);
    this.activeVariable = dt;
  }

}
