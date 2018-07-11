#!/bin/bash

# This script will run all the components in a simple test setup. Can be used 
# to configure the directory after a fresh pull

if [ -z ${D3MCONFIG+x} ]; then 
    echo "D3MCONFIG not set. setting to:" $WCC"/D3M/d3m.cfg"
    export D3MCONFIG=$WCC/D3M/d3m.cfg
fi

export ANT_HOME=/usr/bin/ant
export ANT_HOME=/usr/share/ant
ant -version

 # export PATH=$PATH:$ANT_HOME/bin
# echo $PATH

# if [ -z ${JAVA_HOME+x} ]; then 
    # export JAVA_HOME=/usr
# fi


# Handle help request
if [ "$1" == "--help" ]; then
    echo "Usage: build_component.sh [path_to_workflow_components_dir]"
    exit 0
fi

# Handle the path argument to the runWCC.sh
if [ "$#" -gt 0 ]; then
    if [ ! "$1" == '.' ]; then
        if [[ "$1" = /* ]]; then
            dir="$1"
        else
            dir="$(pwd)"/${1%/}
            # hack to resolve if relative path is given with ../..
            cwd="$(pwd)"
            cd "$dir"
            dir="$(pwd)"
            cd "$cwd"
        fi
    fi
fi

# Check that runWCC.sh is in the directory provided
if [ ! -d "$dir" ]; then
    echo "ERROR: Invalid directory given $dir"
    exit 1
else
    cwd=$(pwd)
    cd "$dir"
    if [ ! -f runWCC.sh ]; then
        echo "ERROR: Invalid directory given. Must provide directory that contains workflow_components" 1>&2
        echo "Path: $dir" 1>&2
        cd "$cwd"
        exit 1
    else
        echo "WorkflowComponents project directory is: $dir"
        cd "$cwd"
    fi
fi
wcc=$dir

# Remove all old workflow components
wf_comps=( DatasetImporter \
    DatasetSelector \
    ProblemCreator \
    ProblemTaskSelector \
    ProblemMetricSelector \
    ProblemGeneratorDefault \
    ModelSearch \
    ModelFit \
    ModelPredict \
    ModelScore \
    ModelSelector \
    CompareModelScores \
)

do_not_build=( \
    VisualizationDescribeData \
    VisualizationConfusionMatrix \
    MetricSelector \
)

cd $cwd
# Go through each module and configure it to run
for f in $(find . -name "build_component.sh"); do
    full_path=$(realpath $f)
    dir=$(dirname $full_path)
    # dir=$(dirname $f)
    echo "##########################################"
    echo "Found component" $dir
    cd $dir 
    # Run configuration scripts
    if [ ! -f src/settings.cfg ]; then
        echo "No settings.cfg file found. Copying from sample"
        cp src/settings.cfg.sample src/settings.cfg
    fi
    # Get component name
    tmp=$IFS
    export IFS="="
    while read -r k v; do
        [ "$k" == "component.name" ] && cname=$v
    done < wcc.properties.template
    echo $cname
    export IFS=$tmp
    # if [[ "${do_not_build[$cname]-X} == "${do_not_build[$cname]}" ]]; then
    if [[ " ${do_not_build[@]} " =~ " $cname " ]]; then
        echo "skipping rebuild of component" $cname
    else
        cdir="$wcc/$cname"
        if [ -d $cdir ]; then
            echo "Removing old generated WC directory" $cdir
            rm -Rf $cdir
        fi
        ./build_component.sh $wcc wcc.properties.template
        cd $cdir
        # ant -version
        ant dist -buildfile $cdir/build.xml
        # buildOutput=`ant dist`
        # echo ${buildOutput} >> build_errors_info.txt
        # antReturnCode=$?

        # echo "ANT: Return code is: \""$antReturnCode"\""

    fi
    echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    cd $cwd
done

