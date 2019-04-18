#!/bin/bash

# Use this script to test the component locally within this folder


# Setup local test folder if necessary
cwd=$(pwd)
echo "CWD: " $cwd
cd build
build_dir="$(pwd)"
echo "build directory: " $build_dir
cd "$cwd"

# Packaging source into "program" directory
$build_dir/setup_run.sh

# Get venv dir
cd $cwd/venv
venv=$(pwd)
cd $cwd
source $venv/bin/activate

# Add all src subdirectories to python path (This emulates the flat heirarch that 
# will exist when this script is run in Tigris
path="$PYTHONPATH""$cwd/program"
echo "Using pythonpath: " $path

PYTHONPATH="$path" python $cwd/src/app.py

deactivate
