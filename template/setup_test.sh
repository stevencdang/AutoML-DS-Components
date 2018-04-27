#!/bin/bash

# This script sets up a local python dev env within this folder for developing the component

# Assumed dependencies:
# -- python pip
# -- python virtualenv
echo "Setting up test env within project folder for development"

virtualenv env --python=python2.7
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

cwd=$(pwd)
if [ ! -d "$cwd/test" ]; then
    mkdir $cwd/test
    echo "Made test directory: '$cwd/test'"
    if [ ! -d "$cwd/test/output" ]; then
        mkdir "$cwd/test/output"
        echo "Made test directory: '$cwd/test/output'"
    fi
fi

# Deactiate python venv
deactivate
