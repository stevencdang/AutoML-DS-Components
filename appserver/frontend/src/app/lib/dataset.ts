import { DataType } from "./dataType"

export class Dataset {

  constructor (
               _id: string,
               dataset_info: DatasetInfo,
               about: DatasetMetadata,
               dataResources: DatasetResource[],
               qualities: qualities
  ) {
  }
};

class DatasetInfo {

  constructor (
    root_path: string,
    dataset_dir: string,
    dataset_schema: string
  ) {}
}

class DatasetMetadata {

  constructor (
    datasetID: string,
    datasetName: string,
    datasetURI: string,
    description: string,
    citation: string,
    publicationDate: string,
    humanSubjectsResearch: string,
    license: string,
    source: string,
    sourceURI: string,
    approximateSize: string,
    applicationDomain: string,
    datasetVersion: string,
    datasetSchemaVersion: string,
    redacted: string,
    digest: string
  ) {}
}

class DatasetResource {
  constructor (
    resID: string,
    resPath: string,
    resType: string,
    resFormat: string,
    isCollection: boolean,
    columns: DataColumn[]
  ) {}
}

class DataColumn {
  constructor (
    colIndex: number,
    colName: string,
    colDescription: string,
    colType: string,
    role: string,
    refersTo: RefDataColumn
  ) {}
}

class RefDataColumn {
  constructor (
    resID: string,
    resObject: string,
    columnIndex: string,
    columnName: string
  ) {}
}

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
