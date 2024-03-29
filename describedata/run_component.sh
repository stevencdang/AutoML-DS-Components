#!/bin/bash

# Use this script to test the component locally within this folder


# Setup local test folder if necessary
cwd=$(pwd)
# Get lib dir
cd ../lib
libdir=$(pwd)
echo "Lib dir: " $libdir
cd $cwd
# Get build_components dir
cd ../build_components
build_dir=$(pwd)
echo "build dir: " $build_dir
cd $cwd
# Get venv dir
cd ../venv
venv=$(pwd)
echo "venv dir: " $venv
cd $cwd

# Setup local test folder if necessary
cwd=$(pwd)
if [ ! -d "$cwd/test" ]; then
    mkdir $cwd/test
    echo "Made test directory: '$cwd/test'"
fi
if [ ! -d "$cwd/test/output" ]; then
    mkdir "$cwd/test/output"
    echo "Made test directory: '$cwd/test/output'"
fi

# Packaging source into "program" directory
$build_dir/setup_run.sh

# Get venv dir
cd ../venv
venv=$(pwd)
cd $cwd
source $venv/bin/activate

# Add all src subdirectories to python path (This emulates the flat heirarch that 
# will exist when this script is run in Tigris
path="$PYTHONPATH":"$cwd/program"


PYTHONPATH="$path" python src/main.py -programDir $cwd -workingDir $cwd/test/output -userId='testuser' -workflowDir='/datashop/dataset_files/workflows/1162' -is_test=1 -file0="$cwd/test/datasetDoc.tsv" 

deactivate
