#!/bin/bash

# Use this script to test the component locally within this folder

source env/bin/activate

# Setup local test folder if necessary
cwd=$(pwd)
# Get lib dir
cd ../lib
libdir=$(pwd)
cd $cwd

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

PYTHONPATH="$path" python src/main.py -programDir $cwd -workingDir $cwd/test/output -file0="$cwd/test/datasetDoc.tsv" -file1=$cwd/test/problemDoc.json -userId=' ' -is_test=1

deactivate
