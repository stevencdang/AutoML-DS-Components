#!/bin/bash

# This script sets up a local python dev env within this folder for developing the component

# Assumed dependencies:
# -- python pip
# -- python virtualenv
echo "Setting up test env for development"

cwd="$(pwd)"
echo "cwd: " $cwd
wcc_dir="$(dirname $cwd)"
echo "wcc: " $wcc_dir
venv="$wcc_dir"/venv
echo "venv: " $venv
build_dir="$wcc_dir/build_components"
echo "build: " $build_dir

if [ ! -d $venv ]; then
    virtualenv $venv --python=python3.6
    source $venv/bin/activate
    pip install --upgrade pip
    pip install -r $build_dir/requirements.txt

    # install d3m ta3ta2-api
    cd ../venv
    mkdir tmp
    cd tmp
    git clone https://gitlab.com/datadrivendiscovery/ta3ta2-api.git
    cd ta3ta2-api
    git checkout dist-python
    python setup.py install
    cd $cwd

    # Deactiate python venv
    deactivate
fi


if [ ! -d "$cwd/test" ]; then
    mkdir $cwd/test
    echo "Made test directory: '$cwd/test'"
    if [ ! -d "$cwd/test/output" ]; then
        mkdir "$cwd/test/output"
        echo "Made test directory: '$cwd/test/output'"
    fi
fi

