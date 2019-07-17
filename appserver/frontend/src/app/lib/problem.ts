
export enum ProblemTaskTypes {
      CLASSIFICATION,
      REGRESSION,
      CLUSTERING,
      LINK_PREDICTION,
      VERTEX_NOMINATION,
      VERTEX_CLASSIFICATION,
      COMMUNITY_DETECTION,
      GRAPH_MATCHING,
      TIME_SERIES_FORECASTING,
      COLLABORATIVE_FILTERING,
      OBJECT_DETECTION,
      SEMISUPERVISED_CLASSIFICATION,
      SEMISUPERVISED_REGRESSION
}

export enum ProblemTaskSubtypes {
  BINARY,
    MULTICLASS,
    MULTILABEL,
    UNIVARIATE,
    MULTIVARIATE,
    OVERLAPPING,
    NONOVERLAPPING
}

export class Problem {
  
  constructor (
    public _id: string,
    public name: string,
    public version: string,
    public description: string,
    public task_type: string,
    public subtype: string,
    public metrics: PerformanceMetric[],
    public dataSplits: ProblemDataSplit,
    public inputs: ProblemInput[],
    public expected_outputs: ProblemOutput,
    public data_aug_parms: AugmentationInfo[]
  ) {}

}

export class ProblemInput {
  constructor (
    public dataset_id: string,
    public targets: ProblemTarget[],
    public privileged_data: PrivilegedData[],
  ) {}
}

//class ProblemData {
  //constructor (
    //public datasetID: string,
    //public targets: ProblemTarget[],
    //public privilegedData: PrivilegedData[]
  //) {}
//}

export class ProblemTarget {
  constructor (
    public resource_id: string,
    public column_index: number,
    public column_name: string,
    public target_index?: number,
    public num_clusters?: number
  ) {}
}

class PrivilegedData {
  constructor (
    public privileged_data_index: number,
    public resource_id: string,
    public col_index: number,
    public col_name: string
  ) {}
}


class ProblemDataSplit {
  constructor (
    public method: string,
    public test_size: number,
    public num_folds: number,
    public stratified: boolean,
    public num_repeats: number,
    public random_seed: number,
    public splits_file: string,
    public split_script: string
  ) {}
}

export class PerformanceMetric {
  constructor (
    public metric: string,
    public K?: number,
    public posLabel?: string
  ) {}
}

class ProblemOutput {
  constructor (
    public predictionsFile: string,
    public scoresFile: string
  ) {}
}

class AugmentationInfo {
  constructor (
    public domain: string[],
    public keywords: string[]
  ) {}
}
