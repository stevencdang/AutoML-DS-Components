
export class WorkflowSession {

  constructor (
      public _id: string,
      public user_id: string,
      public workflow_id: string, 
      public component_type: string,
      public session_url: string
  ) { 
    this._id = _id;
    this.user_id = user_id;
    this.workflow_id = workflow_id;
    this.component_type = component_type;
    this.session_url = session_url;

  }
}

export class SimpleEDASession extends WorkflowSession {

  constructor(
      public _id: string,
      public user_id: string,
      public workflow_id: string, 
      public component_type: string,
      public session_url: string,
      public dataset_id: string
  ) { 
    super(_id, user_id, workflow_id, component_type, session_url);
    this.dataset_id = dataset_id;
  }



}
