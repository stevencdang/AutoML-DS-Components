import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';

import { Dataset } from "../lib/dataset";
import { DatasetIntf } from './dataset';
import { WorkflowSession } from './workflowSession';
import { Problem } from "../lib/problem";

@Injectable({
    providedIn: 'root',
})
export class DataService {
  datasetUrl: string = "/ds/getDataset";
  problemUrl: string = "/prob/getProblem";
  getSessionUrl: string = "/wfs";
  backendAddr: string = "/dexplorer";
  bokehUrl1: string = "/viz/bokeh1";
  bokehUrl2: string = "/viz/testbokeh2";
  constructor(private http: HttpClient) { }

  getDataset(dsid: string): Observable<Dataset> {
    //return "Testing Data Service"
    //return of("Testing Data Service Observable")
    //
    let url: string = this.backendAddr + this.datasetUrl + "/" + dsid;
    console.log("Getting dataset with GET at: ", url);
    return this.http.get<Dataset>(url);
  }

  getProblem(pid: string): Observable<Problem> {
    let url: string = this.backendAddr + this.problemUrl + "/" + pid;
    console.log("Getting problem with GET at: ", url);
    return this.http.get<Problem>(url);
  }

  updateProblem(prob: Problem): Observable<Object> {
    let url: string = this.backendAddr + this.problemUrl + "/" + prob._id;
    const httpoptions = {
      headers: new HttpHeaders({
          'Content-Type':  'application/json'
      })
    };
    console.log("updating problem in db with PUT: ", url);
    let msg = JSON.stringify(prob);
    console.log("Putting json: ", msg);
    return this.http.put<Object>(url, msg, httpoptions);
    
  }



  getWorkflowSession(wfid: string): Observable<Object> {
    let url: string = this.backendAddr + this.getSessionUrl + "/" + wfid;
    console.log("Getting workflow session with GET: ", url);
    return this.http.get<Object>(url);
    
  }

  updateWorkflowSession(wfid: string, updates: Object): Observable<Object> {
    let url: string = this.backendAddr + this.getSessionUrl + "/" + wfid;
    const httpoptions = {
      headers: new HttpHeaders({
          'Content-Type':  'application/json'
      })
    };
    console.log("updating workflow session with PUT: ", url);
    return this.http.put<Object>(url, updates, httpoptions);
    
  }


  testBokeh1(): Observable<Object> {
    return this.http.get(this.bokehUrl1)
  }

  testBokeh2(): Observable<Object> {
    return this.http.get(this.bokehUrl2)
  }

}
