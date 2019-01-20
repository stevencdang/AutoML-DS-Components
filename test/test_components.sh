#!/bin/bash

# This script will run all the components in a simple test setup. Can be used 
# to configure the directory after a fresh pull

if [ -z ${D3MCONFIG+x} ]; then 
    echo "D3MCONFIG not set. setting to:\t"$WCC"/D3M/d3m.cfg"
    export D3MCONFIG=$WCC/D3M/d3m.cfg
fi


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

cwd=$(pwd)
echo "Current working directory" $cwd
log_dir=$cwd/run
echo "Writing logs to" $log_dir

cd ..

if [[ " ${test_comps[@]} " =~ " datasetimporter " ]]; then
    # Test DatasetImporter
    cname=datasetimporter
    cd $cname
    echo "#########################################################"
    echo "Running" $cname
    log_file=$log_dir/$cname.log
    if [ -f $log_file ]; then
        rm $log_file
    fi
    ./run_component.sh &> $log_file
    echo "#########################################################"
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " datasetselector " ]]; then
    # Test DatasetSelector
    cname=datasetselector
    cd $cname
    echo "#########################################################"
    echo "Running" $cname
    log_file=$log_dir/$cname.log
    if [ -f $log_file ]; then
        rm $log_file
    fi
    cp ../datasetimporter/test/output/dataset-list.tsv test/
    ./run_component.sh &> $log_file
    echo "#########################################################"
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " problemgeneratordefault " ]]; then
    # Test ProblemGeneratorDefault
    cname=problemgeneratordefault
    cd $cname
    echo "#########################################################"
    echo "Running" $cname
    log_file=$log_dir/$cname.log
    if [ -f $log_file ]; then
        rm $log_file
    fi
    cp ../datasetselector/test/output/datasetDoc.tsv test/
    ./run_component.sh &> $log_file
    echo "#########################################################"
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " problemcreator " ]]; then
    # Test ProblemCreator
    cname=problemcreator
    cd $cname
    echo "#########################################################"
    echo "Running" $cname
    log_file=$log_dir/$cname.log
    if [ -f $log_file ]; then
        rm $log_file
    fi
    cp ../datasetselector/test/output/datasetDoc.tsv test/
    ./run_component.sh &> $log_file
    echo "#########################################################"
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " problemtaskselector " ]]; then
    # Test ProblemTaskSelector
    cname=problemtaskselector
    cd $cname
    echo "#########################################################"
    echo "Running" $cname
    log_file=$log_dir/$cname.log
    if [ -f $log_file ]; then
        rm $log_file
    fi
    cp ../datasetselector/test/output/datasetDoc.tsv test/
    cp ../problemcreator/test/output/problemTarget.tsv test/
    ./run_component.sh &> $log_file
    echo "#########################################################"
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " problemmetricselector " ]]; then
    # Test ProblemMetricSelector
    cname=problemmetricselector
    cd $cname
    echo "#########################################################"
    echo "Running" $cname
    log_file=$log_dir/$cname.log
    if [ -f $log_file ]; then
        rm $log_file
    fi
    cp ../datasetselector/test/output/datasetDoc.tsv test/
    cp ../problemtaskselector/test/output/problemTask.tsv test/
    ./run_component.sh &> $log_file
    echo "#########################################################"
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " modelsearch " ]]; then
    # Test modelSearch
    cname=modelsearch
    cd $cname
    echo "#########################################################"
    echo "Running" $cname
    log_file=$log_dir/$cname.log
    if [ -f $log_file ]; then
        rm $log_file
    fi
    cp ../datasetselector/test/output/datasetDoc.tsv test/
    if [ -f ../problemgeneratordefault/test/output/problemDoc.json ]; then
        cp ../problemgeneratordefault/test/output/problemDoc.json test/
    elif [ -f ../problemmetricselector/test/output/problemDoc.json ]; then
        cp ../problemmetricselector/test/output/problemDoc.json test/
    else
        echo "Can't run component need to run problem generation components first"
    fi
    ./run_component.sh &> $log_file
    echo "#########################################################"
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " modelfit " ]]; then
    # Test modelFit
    cname=modelfit
    cd $cname
    echo "#########################################################"
    echo "Running" $cname
    log_file=$log_dir/$cname.log
    if [ -f $log_file ]; then
        rm $log_file
    fi
    cp ../datasetselector/test/output/datasetDoc.tsv test/
    cp ../modelsearch/test/output/model-flows.tsv test/
    ./run_component.sh &> $log_file
    echo "#########################################################"
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " modelpredict " ]]; then
    # Test modelpredict
    cname=modelpredict
    cd $cname
    echo "#########################################################"
    echo "Running" $cname
    log_file=$log_dir/$cname.log
    if [ -f $log_file ]; then
        rm $log_file
    fi
    cp ../datasetselector/test/output/datasetDoc.tsv test/
    cp ../modelfit/test/output/fit-models.tsv test/
    ./run_component.sh &> $log_file
    echo "#########################################################"
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " modelscore " ]]; then
    # Test modelscore
    cname=modelscore
    cd $cname
    echo "#########################################################"
    echo "Running" $cname
    log_file=$log_dir/$cname.log
    if [ -f $log_file ]; then
        rm $log_file
    fi
    cp ../datasetselector/test/output/datasetDoc.tsv test/
    cp ../modelsearch/test/output/model-flows.tsv test/
    ./run_component.sh &> $log_file
    echo "#########################################################"
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " modelselector " ]]; then
    # Test modelselector
    cname=modelselector
    cd $cname
    echo "#########################################################"
    echo "Running" $cname
    log_file=$log_dir/$cname.log
    if [ -f $log_file ]; then
        rm $log_file
    fi
    cp ../modelsearch/test/output/model-flows.tsv test/
    ./run_component.sh &> $log_file
    echo "#########################################################"
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " comparemodelscores " ]]; then
    # Test comparemodelscores
    cname=comparemodelscores
    cd visualizations/$cname
    echo "#########################################################"
    echo "Running" $cname
    log_file=$log_dir/$cname.log
    if [ -f $log_file ]; then
        rm $log_file
    fi
    cp ../../modelscore/test/output/model-scores.tsv test/
    ./run_component.sh &> $log_file
    echo "#########################################################"
    cd ../..
fi

if [[ " ${test_comps[@]} " =~ " modelrank " ]]; then
    cname=modelrank
    cd $cname
    echo "#########################################################"
    echo "Running" $cname
    log_file=$log_dir/$cname.log
    if [ -f $log_file ]; then
        rm $log_file
    fi
    cp ../datasetselector/test/output/datasetDoc.tsv test/
    cp ../modelfit/test/output/fit-models.tsv test/
    ./run_component.sh &> $log_file
    echo "#########################################################"
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " modelrerank " ]]; then
    cname=modelrerank
    cd $cname
    echo "#########################################################"
    echo "Running" $cname
    log_file=$log_dir/$cname.log
    if [ -f $log_file ]; then
        rm $log_file
    fi
    cp ../modelrank/test/output/ranked-models.tsv test/
    ./run_component.sh &> $log_file
    echo "#########################################################"
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " modelexport " ]]; then
    cname=modelexport
    cd $cname
    echo "#########################################################"
    echo "Running" $cname
    log_file=$log_dir/$cname.log
    if [ -f $log_file ]; then
        rm $log_file
    fi
    cp ../modelrank/test/output/ranked-models.tsv test/
    ./run_component.sh &> $log_file
    echo "#########################################################"
    cd ..
fi

if [[ " ${test_comps[@]} " =~ " comparemodelpredictions " ]]; then
    # Test describedata
    cname=comparemodelpredictions
    cd visualizations/$cname
    echo "#########################################################"
    echo "Running" $cname
    log_file=$log_dir/$cname.log
    if [ -f $log_file ]; then
        rm $log_file
    fi
    cp ../../datasetselector/test/output/datasetDoc.tsv test/
    if [ -f ../../problemgeneratordefault/test/output/problemDoc.json ]; then
        cp ../../problemgeneratordefault/test/output/problemDoc.json test/
    elif [ -f ../../problemmetricselector/test/output/problemDoc.json ]; then
        cp ../../problemmetricselector/test/output/problemDoc.json test/
    else
        echo "Can't run component need to run problem generation components first"
    fi
    cp ../../modelsearch/test/output/fit-models.tsv test/
    cp ../../modelsearch/test/output/predictions.tsv test/
    ./run_component.sh &> $log_file
    echo "#########################################################"
    cd ../..
fi

if [[ " ${test_comps[@]} " =~ " describedata " ]]; then
    # Test describedata
    cname=describedata
    cd visualizations/$cname
    echo "#########################################################"
    echo "Running" $cname
    log_file=$log_dir/$cname.log
    if [ -f $log_file ]; then
        rm $log_file
    fi
    cp ../../datasetselector/test/output/datasetDoc.tsv test/
    ./run_component.sh &> $log_file
    echo "#########################################################"
    cd ../..
fi

