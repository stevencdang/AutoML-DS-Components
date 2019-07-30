REPLACE INTO `workflow_component` (
    `workflow_component_id`,
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
    1,
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
    `workflow_component_id`,
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
    4,
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
REPLACE INTO `workflow_component` (
    `workflow_component_id`,
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
    11,
	'Analysis',
	'Problem_Creator',
	'/datashop/workflow_components/ProblemCreator/',
	'/datashop/workflow_components/ProblemCreator/schemas/ProblemCreator_v1_0.xsd',
	'/usr/bin/java -jar',
	'/datashop/workflow_components/ProblemCreator/dist/ProblemCreator-1.0.jar', 
	1,
	'system',
	'Steven_C_Dang',
	'1.0', 
	'Allow user to select problem target from columns of a dataset from a dataset repository'
);
REPLACE INTO `workflow_component` (
    `workflow_component_id`,
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
    16,
	'Analysis',
	'Model_Export',
	'/datashop/workflow_components/ModelExport/',
	'/datashop/workflow_components/ModelExport/schemas/ModelExport_v1_0.xsd',
	'/usr/bin/java -jar',
	'/datashop/workflow_components/ModelExport/dist/ModelExport-1.0.jar', 
	1,
	'system',
	'Steven_C_Dang',
	'1.0', 
	'Export models for D3M Evaluation'
);
