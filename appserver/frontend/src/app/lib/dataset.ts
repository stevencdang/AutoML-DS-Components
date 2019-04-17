import { DataType } from "./dataType"

export class Dataset {
  
  columns: DataType[];

  constructor () {
    
    this.columns = [];
    for (let i=0; i<10; i++) {
      let varName: string = `Variable ${i}`;
      let dt: DataType = new DataType(varName);
      this.columns.push(dt); 

    }

  }
}
