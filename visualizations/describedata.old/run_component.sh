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

# Add program directory to pythonpath
path="$PYTHONPATH":"$cwd/program"

PYTHONPATH="$path" python src/main.py -programDir $cwd -workingDir $cwd/test/output -userId=' ' -is_test=1 -file0 "$cwd/test/datasetDoc.tsv"

