import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

import { DatasetIntf } from './dataset';
import { WorkflowSession } from './workflowSession';

@Injectable({
    providedIn: 'root',
})
export class DataService {
  datasetUrl: string = "/ds/getDataset";
  getSessionUrl: string = "/wfs";
  backendAddr: string = "http://localhost:8686";
  bokehUrl1: string = "http://sophia.stevencdang.com:5000/testbokeh1";
  bokehUrl2: string = "http://sophia.stevencdang.com:5000/testbokeh2";
  constructor(private http: HttpClient) { }

  getDataset(dsid: string): Observable<Dataset> {
    //return "Testing Data Service"
    //return of("Testing Data Service Observable")
    //
    let url: string = this.backendAddr + this.datasetUrl + "/" + dsid;
    return this.http.get<Dataset>(url);
  }

  getWorkflowSession(wfid: string): Observable<Object> {
    let url: string = this.backendAddr + this.getSessionUrl + "/" + wfid;
    console.log("Getting workflow session with GET: ", url);
    return this.http.get<Object>(url);
    
  }

  updateWorkflowSession(wfid: string, updates: Object): Observable<Object> {
    let url: string = this.backendAddr + this.getSessionUrl + "/" + wfid;
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    console.log("updating workflow session with PUT: ", url);
    return this.http.put<Object>(url, updates, {headers: headers});
    
  }


  testBokeh1(): Observable<Object> {
    return this.http.get(this.bokehUrl1)
  }

  testBokeh2(): Observable<Object> {
    return this.http.get(this.bokehUrl2)
  }

}
