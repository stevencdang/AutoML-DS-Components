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

    cd $cwd

    # Deactiate python venv
    deactivate
fi

