REPLACE INTO `workflow_component` (
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
	'Compare_Model_Predictions',
	'/datashop/workflow_components/CompareModelPredictions/',
	'/datashop/workflow_components/CompareModelPredictions/schemas/CompareModelPredictions_v1_0.xsd',
	'/usr/bin/java -jar',
	'/datashop/workflow_components/CompareModelPredictions/dist/CompareModelPredictions-1.0.jar', 
	1,
	'system',
	'Steven_C_Dang',
	'1.0', 
	'Create Visualization of errors of each model given'
);
