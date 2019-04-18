import { DataType } from "./dataType"

export class Dataset {
  id: string; 
  columns: DataAttribute[];

  constructor (dsid: string, columns: DataAttribute[]) {
  //constructor (dsid: string) {
    this.id = dsid
    this.columns = columns
    
  }


};

export function datasetFromJson(d): Dataset {
  var cols: DataAttribute[] = [];
  for (var col of d['DatasetColumns']) {
    //console.log(JSON.parse(col))
    let c = JSON.parse(col);
    cols.push(new DataAttribute(
      d['DatasetId'],
      c['colName'],
      c['colIndex'],
      c['colType'],
      c['roles']
    ));
  }
  
  return new Dataset(d['DatasetId'], cols);

}

export interface DatasetIntf  extends Dataset {
  DatasetId: string;
  DatasetColumns: DataAttribute[];
}

export class DataAttribute {
  //name: string;
  //index: number;
  //datatype: string;
  //roles: string[];

  constructor(public datasetId: string, 
              public colName: string,
              public colIndex: number,
              public colType: string,
              public roles: string[]) {
  }
}
