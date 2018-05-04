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

# Add all src subdirectories to python path (This emulates the flat heirarch that 
# will exist when this script is run in Tigris
path="$PYTHONPATH"
for dir in $(find src -type d); do
    path="$path:$dir"
done

PYTHONPATH="$path" python src/main.py -programDir $cwd/src -workingDir $cwd/test/output -userId=' ' -is_test=1



