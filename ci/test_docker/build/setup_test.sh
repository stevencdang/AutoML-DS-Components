#!/bin/bash

# This script sets up a local python dev env within this folder for developing the component

# Assumed dependencies:
# -- python pip
# -- python virtualenv
echo "Setting up test env for development"
cwd="$(pwd)"
echo "cwd: " $cwd
cd $cwd/build
build_dir="$(pwd)"
echo "build directory: " $build_dir
cd ..
base_dir="$(pwd)"
echo "base directory: " $base_dir
venv="$base_dir"/venv
echo "venv: " $venv

if [ ! -d $venv ]; then
    virtualenv $venv --python=python3.6
    source $venv/bin/activate
    pip install --upgrade pip
    pip install -r $build_dir/requirements.txt

    # install d3m ta3ta2-api
    cd $base_dir/venv
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

