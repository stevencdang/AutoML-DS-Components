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
	'Problem_Task_Selector',
	'/datashop/workflow_components/ProblemTaskSelector/',
	'/datashop/workflow_components/ProblemTaskSelector/schemas/ProblemTaskSelector_v1_0.xsd',
	'/usr/bin/java -jar',
	'/datashop/workflow_components/ProblemTaskSelector/dist/ProblemTaskSelector-1.0.jar', 
	1,
	'system',
	'Steven_C_Dang',
	'1.0', 
	'Allow user to select problem task for a given problem target'
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
	'Problem_Metric_Selector',
	'/datashop/workflow_components/ProblemMetricSelector/',
	'/datashop/workflow_components/ProblemMetricSelector/schemas/ProblemMetricSelector_v1_0.xsd',
	'/usr/bin/java -jar',
	'/datashop/workflow_components/ProblemMetricSelector/dist/ProblemMetricSelector-1.0.jar', 
	1,
	'system',
	'Steven_C_Dang',
	'1.0', 
	'Allow user to select a metric to use for the problem'
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
	'Model_Score',
	'/datashop/workflow_components/ModelScore/',
	'/datashop/workflow_components/ModelScore/schemas/ModelScore_v1_0.xsd',
	'/usr/bin/java -jar',
	'/datashop/workflow_components/ModelScore/dist/ModelScore-1.0.jar', 
	1,
	'system',
	'Steven_C_Dang',
	'1.0', 
	'Allow user to evaluate the performance of a set of models'
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
	'Model_Fit',
	'/datashop/workflow_components/ModelFit/',
	'/datashop/workflow_components/ModelFit/schemas/ModelFit_v1_0.xsd',
	'/usr/bin/java -jar',
	'/datashop/workflow_components/ModelFit/dist/ModelFit-1.0.jar', 
	1,
	'system',
	'Steven_C_Dang',
	'1.0', 
	'Allow user to fit a model using a dataset'
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
	'Model_Predict',
	'/datashop/workflow_components/ModelPredict/',
	'/datashop/workflow_components/ModelPredict/schemas/ModelPredict_v1_0.xsd',
	'/usr/bin/java -jar',
	'/datashop/workflow_components/ModelPredict/dist/ModelPredict-1.0.jar', 
	1,
	'system',
	'Steven_C_Dang',
	'1.0', 
	'Allow user to generate predictions on a dataset given a fitted model'
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
	'Model_Selector',
	'/datashop/workflow_components/ModelSelector/',
	'/datashop/workflow_components/ModelSelector/schemas/ModelSelector_v1_0.xsd',
	'/usr/bin/java -jar',
	'/datashop/workflow_components/ModelSelector/dist/ModelSelector-1.0.jar', 
	1,
	'system',
	'Steven_C_Dang',
	'1.0', 
	'Allow user to select a model from a list of models'
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
	'Visualization',
	'Compare_Model_Scores',
	'/datashop/workflow_components/CompareModelScores/',
	'/datashop/workflow_components/CompareModelScores/schemas/CompareModelScores_v1_0.xsd',
	'/usr/bin/java -jar',
	'/datashop/workflow_components/CompareModelScores/dist/CompareModelScores-1.0.jar', 
	1,
	'system',
	'Steven_C_Dang',
	'1.0', 
	'Generates an interactive html barplot comparing given model scores'
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
	'Model_Selector',
	'/datashop/workflow_components/ModelSelector/',
	'/datashop/workflow_components/ModelSelector/schemas/ModelSelector_v1_0.xsd',
	'/usr/bin/java -jar',
	'/datashop/workflow_components/ModelSelector/dist/ModelSelector-1.0.jar', 
	1,
	'system',
	'Steven_C_Dang',
	'1.0', 
	'Allow user to select a model from a list of models'
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
	'Rank_Models',
	'/datashop/workflow_components/ModelRank/',
	'/datashop/workflow_components/ModelRank/schemas/ModelRank_v1_0.xsd',
	'/usr/bin/java -jar',
	'/datashop/workflow_components/ModelRank/dist/ModelRank-1.0.jar', 
	1,
	'system',
	'Steven_C_Dang',
	'1.0', 
	'Allow user to rank a set of models using performance along a metric'
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
	'Model_Rerank',
	'/datashop/workflow_components/ModelRerank/',
	'/datashop/workflow_components/ModelRerank/schemas/ModelRerank_v1_0.xsd',
	'/usr/bin/java -jar',
	'/datashop/workflow_components/ModelRerank/dist/ModelRerank-1.0.jar', 
	1,
	'system',
	'Steven_C_Dang',
	'1.0', 
	'Allow user to manually specify the rank of a model from an ordered list of ranked models'
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
	'Visualization',
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
	'Visualization',
	'Describe_Data',
	'/datashop/workflow_components/DescribeData/',
	'/datashop/workflow_components/DescribeData/schemas/DescribeData_v1_0.xsd',
	'/usr/bin/java -jar',
	'/datashop/workflow_components/DescribeData/dist/DescribeData-1.0.jar', 
	1,
	'system',
	'Steven_C_Dang',
	'1.0', 
	'Create exploratory data graphs for a given dataset'
);
