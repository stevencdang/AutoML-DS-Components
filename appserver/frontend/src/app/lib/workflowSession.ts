
export class WorkflowSession {

  constructor (
      public _id: string,
      public user_id: string,
      public workflow_id: string, 
      public comp_id: string,
      public comp_type: string,
      public state: string,
      public session_url: string
  ) { 
    this._id = _id;
    this.user_id = user_id;
    this.workflow_id = workflow_id;
    this.comp_id = comp_id;
    this.comp_type = comp_type;
    this._id = _id;
    this.state = state;
    this.session_url = session_url;

  }
}

export class SimpleEDASession extends WorkflowSession {

  constructor(
      public _id: string,
      public user_id: string,
      public workflow_id: string, 
      public comp_id: string,
      public comp_type: string,
      public state: string,
      public session_url: string,
      public dataset_id: string
  ) { 
    super(_id, user_id, workflow_id, comp_id, comp_type, state, session_url);
    this.dataset_id = dataset_id;
  }

}

export class DatasetImporterSession extends WorkflowSession {

  constructor(
      public _id: string,
      public user_id: string,
      public workflow_id: string, 
      public comp_id: string,
      public comp_type: string,
      public state: string,
      public session_url: string,
      public dataset_id: string,
      public available_datasets: string[]

  ) { 
    super(_id, user_id, workflow_id, comp_id, comp_type, state, session_url);
    this.dataset_id = dataset_id;
    this.available_datasets = available_datasets
  }

  is_changed(dsid: string) {
    console.log("Checking dataset id ", dsid, 
      "if different from dataset id from workflow session: ", this.dataset_id);
    return dsid != this.dataset_id;
  }
}

export class ProblemCreatorSession extends WorkflowSession {

  constructor(
    public _id: string,
    public user_id: string,
    public workflow_id: string, 
    public comp_id: string,
    public comp_type: string,
    public state: string,
    public session_url: string,
    public dataset_id: string,
    public input_wfids: string[],
    public prob_id: string,
    public prob_state: object,
    public suggest_pids: string[]
  ) { 
    super(_id, user_id, workflow_id, comp_id, comp_type, state, session_url);
    //this.dataset_id = dataset_id;
    //this.input_wfids = input_wfids;
  }
}
