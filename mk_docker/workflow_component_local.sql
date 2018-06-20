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
	'Dataset_Importer',
	'/datashop/workflow_components/DatasetImporter/',
	'/datashop/workflow_components/DatasetImporter/schemas/DatasetImporter_v1_0.xsd',
	'/usr/bin/java -jar',
	'/datashop/workflow_components/DatasetImporter/dist/DatasetImporter-1.0.jar', 
	1,
	'system',
	'Steven_C_Dang',
	'1.0', 
	'Make a dataset repository available within a workflow to select datasets'
);
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
	'Dataset_Selector',
	'/datashop/workflow_components/DatasetSelector/',
	'/datashop/workflow_components/DatasetSelector/schemas/DatasetSelector_v1_0.xsd',
	'/usr/bin/java -jar',
	'/datashop/workflow_components/DatasetSelector/dist/DatasetSelector-1.0.jar', 
	1,
	'system',
	'Steven_C_Dang',
	'1.0', 
	'Allow user to select a dataset from a dataset repository'
);
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
	'Default_Problem_Generator',
	'/datashop/workflow_components/ProblemGeneratorDefault/',
	'/datashop/workflow_components/ProblemGeneratorDefault/schemas/ProblemGeneratorDefault_v1_0.xsd',
	'/usr/bin/java -jar',
	'/datashop/workflow_components/ProblemGeneratorDefault/dist/ProblemGeneratorDefault-1.0.jar', 
	1,
	'system',
	'Steven_C_Dang',
	'1.0', 
	'Generate the default problem for each dataset'
);
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
	'Model_Search',
	'/datashop/workflow_components/ModelSearch/',
	'/datashop/workflow_components/ModelSearch/schemas/ModelSearch_v1_0.xsd',
	'/usr/bin/java -jar',
	'/datashop/workflow_components/ModelSearch/dist/ModelSearch-1.0.jar', 
	1,
	'system',
	'Steven_C_Dang',
	'1.0', 
	'Allow the user to search for a model given no previous model'
);
