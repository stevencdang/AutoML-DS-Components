INSERT INTO `workflow_component` (
    `component_type`, 
    `component_name`, 
    `tool_dir`, 
    `schema_path`, 
    `interpreter_path`, 
    `tool_path`, 
    `enabled`, 
    `author`, 
    `citation`, 
    `version`, 
    `info`
) 
VALUES (
    'Analysis', 
    'D3m_Dataset', 
    '/datashop/workflow_components/D3mDatasetSelector/', 
    '/datashop/workflow_components/D3mDatasetSelector/schemas/D3mDatasetSelector_v1_0.xsd', 
    '/usr/bin/java -jar', 
    '/datashop/workflow_components/D3mDatasetSelector/dist/D3mDatasetSelector-1.0.jar', 
    1, 
    'system', 
    'Steven_C_Dang', 
    '1.0', 
    'Component to import a D3M Dataset into the workspace to be manipulated'
);
