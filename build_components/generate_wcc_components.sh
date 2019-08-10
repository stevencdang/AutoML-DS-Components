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

echo "CWD: " $cwd
echo "dir: " $dir

# Check that runWCC.sh is in the directory provided
if [ ! -d "$dir" ]; then
    echo "ERROR: Invalid directory given"  $dir
    exit 1
else
    cwd=$(pwd)
    cd "$dir"
    if [ ! -f runWCC.sh ]; then
        echo "ERROR: Invalid directory given. Must provide directory that contains workflow_components" 
        echo "Path:" $dir
        cd "$cwd"
        exit 1
    else
        echo "WorkflowComponents project directory is: $dir"
        cd "$cwd"
    fi
fi

# Ensure current workign director is the base directory of the project
if [ $(basename $(pwd)) == "build_components" ]; then
    echo "Current directory is build directory. Changing to parent to run script"
    
    cwd="$(dirname $(pwd))"
    cd $cwd
else 
    if [ ! -d "build_components" ]; then
        echo "Current directory is not base directory of components. Please run from base directory" 
        exit 1
    fi
fi

wcc=$dir
echo "WCC is set to director: " $wcc

# set build directory
build_dir="$(pwd)/build_components"
echo "Build directory " $build_dir

# Remove all old workflow components
wf_comps=( \
    DatasetImporter \
    ProblemCreator \
    ModelSearch \
    ModelExport \
)

do_not_build=( \
    CompareModelScores \
    CompareModelPredictions \
    DatasetAugmenter \
    DatasetSelector \
    VisualizationDescribeData \
    VisualizationConfusionMatrix \
    ModelPredict \
    ModelScore \
    ModelFit \
    ModelSelector \
    ModelRank \
    ModelRerank \
    DescribeData \
)

cd $cwd
# Go through each module and configure it to run
for f in $(find . -name "wcc.properties.template"); do
    full_path=$(realpath $f)
    dir=$(dirname $full_path)
    # dir=$(dirname $f)
    echo "################# CG #######################"
    echo "full path " $full_path
    echo "Found component" $dir
    cd $dir 

    # Run configuration scripts
    if [ ! -f src/settings.cfg ]; then
        echo "No settings.cfg file found. Copying from sample"
        cp src/settings.cfg.sample src/settings.cfg
    fi

    # Get component name
    if [ -f $dir/component.properties ]; then
        tmp=$IFS
        export IFS="="
        while read -r k v; do
            [ "$k" == "component.name" ] && cname=$v
        done < $dir/component.properties
        echo $cname
        # Restore default system delmiter
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
            cd $build_dir
            $build_dir/build_component.sh $wcc $dir/wcc.properties.template
            cd $cdir
            ant -version
            ant dist -buildfile $cdir/build.xml
            # buildOutput=`ant dist`
            # echo ${buildOutput} >> build_errors_info.txt
            antReturnCode=$?
            if [ $antReturnCode -ne 0 ]; then
                echo "Error encountered while genarating component: " $cname
            fi

            # echo "ANT: Return code is: \""$antReturnCode"\""

        fi
    else
        echo "No component.properties file. Skipping component"
    fi


    echo "@@@@@@@@@@@@@@@@@ CG @@@@@@@@@@@@@@@@@@@@"
    cd $cwd
done

