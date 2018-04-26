#!/bin/bash

# Use this script to test the component locally within this folder

source env/bin/activate

# Setup local test folder if necessary
cwd=$(pwd)
if [ ! -d "$cwd/test" ]; then
    mkdir $cwd/test
    echo "Made test directory: '$cwd/test'"
    if [ ! -d "$cwd/test/output" ]; then
        mkdir "$cwd/test/output"
        echo "Made test directory: '$cwd/test/output'"
    fi
fi


python program/main.py -programDir $cwd/program -workingDir $cwd/test/output -ds_name='185_baseball' -userId=' ' -is_test=1

