#!/bin/bash

# This script will run all the components in a simple test setup. Can be used 
# to configure the directory after a fresh pull

# look of arguments for which components to test were given
if [ "$#" -gt 0 ]; then
    test_comps="$@"
else
    test_comps=(datasetimporter \
        datasetselector \
        problemgeneratordefault \
        problemcreator \
        problemtaskselector \
        problemmetricselector \
        modelsearch \
        modelfit \
        modelpredict \
        modelscore \
        modelselector \
        comparemodelscores \
        )
fi

echo "Testing components:" $test_comps

cd ..


if [[ " ${test_comps[@]} " =~ " datasetimporter " ]]; then
    # Test DatasetImporter
    cd datasetimporter
    echo "Running datasetimporter"
    ./run_component.sh > ../test/run/datasetimporter.log
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " datasetselector " ]]; then
    # Test DatasetSelector
    cd datasetselector
    echo "Running datasetselector"
    cp ../datasetimporter/test/output/dataset-list.tsv test/
    ./run_component.sh > ../test/run/datasetselector.log
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " problemgeneratordefault " ]]; then
    # Test ProblemGeneratorDefault
    cd problemgeneratordefault
    echo "Running problemgeneratordefault"
    cp ../datasetselector/test/output/datasetDoc.tsv test/
    ./run_component.sh > ../test/run/problemgeneratordefault.log
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " problemcreator " ]]; then
    # Test ProblemCreator
    cd problemcreator
    echo "Running problemcreator"
    cp ../datasetselector/test/output/datasetDoc.tsv test/
    ./run_component.sh > ../test/run/problemcreator.log
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " problemtaskselector " ]]; then
    # Test ProblemTaskSelector
    cd problemtaskselector
    echo "Running problemtaskselector"
    cp ../datasetselector/test/output/datasetDoc.tsv test/
    cp ../problemcreator/test/output/problemTarget.tsv test/
    ./run_component.sh > ../test/run/problemtaskselector.log
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " problemmetricselector " ]]; then
    # Test ProblemMetricSelector
    cd problemmetricselector
    echo "Running problemmetricselector"
    cp ../datasetselector/test/output/datasetDoc.tsv test/
    cp ../problemtaskselector/test/output/problemTask.tsv test/
    ./run_component.sh > ../test/run/problemmetricselector.log
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " modelsearch " ]]; then
    # Test modelSearch
    cd modelsearch
    echo "Running modelsearch"
    cp ../datasetselector/test/output/datasetDoc.tsv test/
    cp ../problemmetricselector/test/output/problemDoc.tsv test/
    ./run_component.sh > ../test/run/modelsearch.log
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " modelfit " ]]; then
    # Test modelFit
    cd modelfit
    echo "Running modelfit"
    cp ../datasetselector/test/output/datasetDoc.tsv test/
    cp ../modelsearch/test/output/model-flows.tsv test/
    ./run_component.sh > ../test/run/modelfit.log
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " modelpredict " ]]; then
    # Test modelpredict
    cd modelpredict
    echo "Running modelpredict"
    cp ../datasetselector/test/output/datasetDoc.tsv test/
    cp ../modelfit/test/output/fit-models.tsv test/
    ./run_component.sh > ../test/run/modelpredict.log
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " modelscore " ]]; then
    # Test modelscore
    cd modelscore
    echo "Running modelscore"
    cp ../datasetselector/test/output/datasetDoc.tsv test/
    cp ../modelsearch/test/output/model-flows.tsv test/
    ./run_component.sh > ../test/run/modelscore.log
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " modelselector " ]]; then
    # Test modelselector
    cd modelselector
    echo "Running modelselector"
    cp ../modelsearch/test/output/model-flows.tsv test/
    ./run_component.sh > ../test/run/modelselector.log
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " comparemodelscores " ]]; then
    # Test comparemodelscores
    cd visualizations/comparemodelscores
    echo "Running comparemodelscores"
    cp ../modelscore/test/output/model-scores.tsv test/
    ./run_component.sh > ../test/run/comparemodelscores.log
    cd ../..
fi
