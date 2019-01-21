#!/bin/bash

# Use this script to test the component locally within this folder

source env/bin/activate

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
./setup_run.sh

# Add all src subdirectories to python path (This emulates the flat heirarch that 
# will exist when this script is run in Tigris
path="$PYTHONPATH":"$cwd/program"

# PYTHONPATH="$path" python src/main.py -programDir $cwd -workingDir $cwd/test/output -ds_name='Amazon product co-purchasing network and ground-truth communities' -file0=$cwd/test/dataset-list.tsv -userId=' ' -is_test=1
PYTHONPATH="$path" python src/main.py -programDir $cwd -workingDir $cwd/test/output -ds_name='acled' -file0=$cwd/test/dataset-list.tsv -userId=' ' -is_test=1

