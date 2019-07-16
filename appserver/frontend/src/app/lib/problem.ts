
export class Problem {

  constructor (
    public _id: string,
    public about: ProblemInfo,
    public inputs: ProblemInput,
    public expectedOutputs: ProblemOutput,
    public dataAugmentation: AugmentationInfo[]
  ) {}

}

class ProblemInfo {
  constructor (
    public problemID: string,
    public problemName: string,
    public problemDescription: string,
    public problemURI: string,
    public taskType: string,
    public taskSubType: string,
    public problemVersion: string,
    public problemSchemaVersion: string
  ) {}
}

class ProblemInput {
  constructor (
    public data: ProblemData,
    public dataSplits: ProblemDataSplit,
    public performanceMetrics: PerformanceMetric[]
  ) {}
}

class ProblemData {
  constructor (
    public datasetID: string,
    public targets: ProblemTarget[],
    public privilegedData: PrivilegedData[]
  ) {}
}

class ProblemTarget {
  constructor (
    public targetIndex: number,
    public resID: string,
    public colIndex: string,
    public colName: string,
    public numClusters: number
  ) {}
}

class PrivilegedData {
  constructor (
    public privilegedDataIndex: number,
    public resID: string,
    public colIndex: string,
    public colName: string
  ) {}
}


class ProblemDataSplit {
  constructor (
    public method: string,
    public testSize: number,
    public numFolds: number,
    public stratified: boolean,
    public numRepeats: number,
    public randomSeed: number,
    public splitsFile: string,
    public splitScript: string
  ) {}
}

class PerformanceMetric {
  constructor (
    public metric: string,
    public K: number,
    public posLabel: string
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
