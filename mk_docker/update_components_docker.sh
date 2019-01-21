#!/bin/bash
# Carnegie Mellon University, Human-Computer Interaction Institute.
# Copyright 2016. All Rights Reserved.
#
# Purpose: Creates the build.properties <<EOF for CMU RHEL servers.
#

BASE=/datashop
DEPLOY=${BASE}/deploy
DATASET_FILES=${BASE}/dataset_files

workflowComponentsBaseDir=${BASE}/workflow_components
rm ${workflowComponentsBaseDir}/build.xml
cd ${workflowComponentsBaseDir}

cat > ImportDiscourseDB/build.properties <<EOF
component.interpreter.path=
component.program.path=program/run.sh
EOF

cat > RLMFitting/build.properties <<EOF
component.interpreter.path=/usr/local/bin/Rscript
component.program.path=program/RLMFitting.R
EOF

cat > AnalysisTkt/build.properties <<EOF
component.interpreter.path=/usr/local/bin/Rscript
component.program.path=program/TKT-model.R
EOF

cat > AnalysisPfa/build.properties <<EOF
component.interpreter.path=/usr/local/bin/Rscript
component.program.path=program/PFA-model.R
EOF

cat > GenerateTktFeatures/build.properties <<EOF
component.interpreter.path=/usr/local/bin/Rscript
component.program.path=program/TKT-features.R
EOF

cat > AnalysisBkt/build.properties <<EOF
executable.dir=/datashop/workflow_components/AnalysisBkt/program/
EOF

cat > GeneratePfaFeatures/build.properties <<EOF
component.interpreter.path=/usr/local/bin/Rscript
component.program.path=program/PFA-features.R
EOF

cat > AnalysisPyAfm/build.properties <<EOF
component.interpreter.path=/usr/local/bin/python3.6
component.program.path=program/afms_workflow_predict.py
EOF

cat > Featuretools-MOOCdb/build.properties <<EOF
component.interpreter.path=/usr/bin/python2.7
component.program.path=program/main.py
EOF

cat > RTemplate/build.properties <<EOF
component.interpreter.path=/usr/local/bin/Rscript
component.program.path=program/analysis.R
EOF

cat > AnalysisRglm/build.properties <<EOF
component.interpreter.path=/usr/local/bin/Rscript
component.program.path=program/R_GLM.R
EOF

cat > TransformPivot/build.properties <<EOF
component.interpreter.path=/usr/local/bin/Rscript
component.program.path=program/pivot.R
EOF

# Coursera/MOOCdb components
cat > CourseraMOOCdbTranslate/build.properties <<EOF
component.interpreter.path=/usr/bin/python2.7
component.program.path=program/piping_scripts/run_coursera.py
EOF

cat > CourseraMOOCdbTranslate/program/ConfigFile.properties <<EOF
[database]
dbHost=127.0.0.1
dbPort=3306
EOF

cat > MOOCdbFeatureExtract/build.properties <<EOF
component.interpreter.path=/usr/bin/python2.7
component.program.path=program/piping_scripts/main.py
EOF

# All Tetrad build.properties get the same run.sh line
for tetradDir in `ls -1d Tetrad*`; do
 cat > ${tetradDir}/build.properties <<EOF
component.interpreter.path=
component.program.path=program/run.sh
EOF
done ;

# More Tetrad, different naming scheme
cat > RowOperations/build.properties <<EOF
component.interpreter.path=
component.program.path=program/run.sh
EOF

cat > GraphEditor/build.properties <<EOF
component.interpreter.path=
component.program.path=program/run.sh
EOF

# New, as of v10.1
cat > DetectorTester/build.properties <<EOF
component.interpreter.path=/usr/bin/node
component.program.path=program/CTAT-detector-plugins/Test_Rig/Test_Rig_WorkflowComponent.js
authorizationProject=ApplyDetectorAccess
detectorsDataset=Detectors
EOF

cat > RowRemover/build.properties <<EOF
component.interpreter.path=/usr/local/bin/Rscript
component.program.path=program/rowRemover.R
EOF

cat > OutputComparator/build.properties <<EOF
component.interpreter.path=/usr/local/bin/Rscript
component.program.path=program/outputComparator.R
EOF

cat > AnalysisDash/build.properties <<EOF
component.interpreter.path=/usr/local/bin/Rscript
component.program.path=program/Dash.R
EOF

# New, as of v10.2
cat > AnalysisIAfm/build.properties <<EOF
component.interpreter.path=/usr/local/bin/Rscript
component.program.path=program/iAFM.R
EOF

cat > TransformClassifyLightside/build.properties <<EOF
component.interpreter.path=/usr/local/bin/python3.6
component.program.path=program/predict.py
EOF

cd ${workflowComponentsBaseDir}/TransformClassifyLightside
ant install
cd ${workflowComponentsBaseDir}

cat > Anonymize/build.properties <<EOF
component.interpreter.path=/usr/bin/node
component.program.path=program/hash.js
EOF

cat > AnalysisIAfm/build.properties <<EOF
component.interpreter.path=/usr/local/bin/Rscript
component.program.path=program/iAFM.R
EOF

#cd ${workflowComponentsBaseDir}/Anonymize/program/
#npm init
#npm install papaparse
#npm install sjcl
#chown :datashop -R ${workflowComponentsBaseDir}/Anonymize/program

cd ${workflowComponentsBaseDir}

cat > DatastageAggregator/build.properties <<EOF
component.interpreter.path=/usr/local/bin/python3.6
component.program.path=program/DatastageAggregator.py
EOF

# New, as of v10.3
cat > OliLoToKc/build.properties <<EOF
component.interpreter.path=/usr/bin/php
component.program.path=program/kc_builder_process.php
sqlite.path=/usr/bin/sqlite3
EOF

cat > EntitySet/build.properties <<EOF
component.interpreter.path=/usr/local/bin/python3.6
component.program.path=program/main.py
EOF

cat > FeatureSynthesis/build.properties <<EOF
component.interpreter.path=/usr/local/bin/python3.6
component.program.path=program/main.py
EOF

cat > TextConverter/build.properties <<EOF
component.interpreter.path=
component.program.path=csvjson
EOF

cat > QAAllElements/build.properties <<EOF
component.interpreter.path=/usr/local/bin/python3.6
component.program.path=program/QAAllElements.py
EOF

cat > QAMultiConnInput/build.properties <<EOF
component.interpreter.path=/usr/local/bin/python3.6
component.program.path=program/QAMultiConnInput.py
EOF


cat > UnzipTemplate/build.properties <<EOF
component.interpreter.path=/usr/local/bin/Rscript
component.program.path=program/analysis.R
EOF

# Compile BKT's programs for this platform
cd AnalysisBkt/program/standard-bkt-public-standard-bkt
make
cp predicthmm ../predicthmm.exe
cp trainhmm ../trainhmm.exe
chmod ug+rx ../predicthmm.exe
chmod ug+rx ../trainhmm.exe

cd ${workflowComponentsBaseDir}
# Copy the app context for components which use the DataShop DAO
# cp ${DEPLOY}/applicationContext.xml CommonLibraries/
cp ${DEPLOY}/datashop.jar CommonLibraries/
#cp ${DEPLOY}/datalab.jar CommonLibraries/

# Build jars
${workflowComponentsBaseDir}/build.sh
