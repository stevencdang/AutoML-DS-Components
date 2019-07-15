import { DataType } from "./dataType"

export class Dataset {

  constructor (
               public _id: string,
               public dataset_info: DatasetInfo,
               public about: DatasetMetadata,
               public dataResources: DatasetResource[],
               public qualities: string
  ) {
  }
};

class DatasetInfo {

  constructor (
    public root_path: string,
    public dataset_dir: string,
    public dataset_schema: string
  ) {}
}

class DatasetMetadata {

  constructor (
    public datasetID: string,
    public datasetName: string,
    public datasetURI: string,
    public description: string,
    public citation: string,
    public publicationDate: string,
    public humanSubjectsResearch: string,
    public license: string,
    public source: string,
    public sourceURI: string,
    public approximateSize: string,
    public applicationDomain: string,
    public datasetVersion: string,
    public datasetSchemaVersion: string,
    public redacted: string,
    public digest: string
  ) {}
}

export class DatasetResource {
  constructor (
    public resID: string,
    public resPath: string,
    public resType: string,
    public resFormat: string,
    public isCollection: boolean,
    public columns: DataColumn[]
  ) {}
}

class DataColumn {
  constructor (
    public colIndex: number,
    public colName: string,
    public colDescription: string,
    public colType: string,
    public role: string,
    public refersTo: RefDataColumn
  ) {}
}

class RefDataColumn {
  constructor (
    public resID: string,
    public resObject: string,
    public columnIndex: string,
    public columnName: string
  ) {}
}

//export function datasetFromJson(d): Dataset {
  //var cols: DataAttribute[] = [];
  //for (var col of d['DatasetColumns']) {
    ////console.log(JSON.parse(col))
    //let c = JSON.parse(col);
    //cols.push(new DataAttribute(
      //d['DatasetId'],
      //c['colName'],
      //c['colIndex'],
      //c['colType'],
      //c['roles']
    //));
  //}
  
  //return new Dataset(d['DatasetId'], cols);

//}

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
