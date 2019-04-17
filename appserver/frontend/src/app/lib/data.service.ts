import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class DataService {
  datasetUrl = 'http://sophia.stevencdang.com:5000';
  constructor(private http: HttpClient) { }

  getDataset(): Observable<Object> {
    //return "Testing Data Service"
    //return of("Testing Data Service Observable")
    //
    return this.http.get(this.datasetUrl);
  }
}
