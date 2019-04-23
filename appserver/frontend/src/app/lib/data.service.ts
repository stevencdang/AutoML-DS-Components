import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

import { DatasetIntf } from './dataset';

@Injectable({
    providedIn: 'root',
})
export class DataService {
  datasetUrl: string = "/ds/getDataCols";
  backendAddr: string = "http://sophia.stevencdang.com:5000";
  bokehUrl1: string = "http://sophia.stevencdang.com:5000/testbokeh1";
  bokehUrl2: string = "http://sophia.stevencdang.com:5000/testbokeh2";
  constructor(private http: HttpClient) { }

  getDataset(): Observable<DatasetIntf> {
    //return "Testing Data Service"
    //return of("Testing Data Service Observable")
    //
    let url: string = this.backendAddr + this.datasetUrl;
    return this.http.get<DatasetIntf>(url);
  }

  getWorkflowSession(wfid): Observable<Object> {
    return this.http.get<DatasetIntf>(this.datasetUrl);
    
  }

  testBokeh1(): Observable<Object> {
    return this.http.get(this.bokehUrl1)
  }

  testBokeh2(): Observable<Object> {
    return this.http.get(this.bokehUrl2)
  }

}
