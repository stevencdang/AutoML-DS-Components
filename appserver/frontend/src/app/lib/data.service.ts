import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

import { DatasetIntf } from './dataset';

@Injectable({
    providedIn: 'root',
})
export class DataService {
  datasetUrl: string = "http://sophia.stevencdang.com:5000/ds/getDataCols";
  constructor(private http: HttpClient) { }

  getDataset(): Observable<DatasetIntf> {
    //return "Testing Data Service"
    //return of("Testing Data Service Observable")
    //
    return this.http.get<DatasetIntf>(this.datasetUrl);
  }
}
