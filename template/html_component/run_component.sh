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
srcdir=$(pwd)
echo "Packaging python source to be built into 'program' directory: $srcdir/program"
if [ ! -d "$srcdir"/program ]; then
    mkdir "$srcdir"/program
else
    # Clean out the old source before continuing
    rm -R "$srcdir"/program
    mkdir "$srcdir"/program
fi
# Copy all source files to the "program" folder for runWCC.sh to copy into new component folder
cd $srcdir/src
# Replicate directory structure
find "$srcdir"/src -mindepth 1 -type d -printf %P\\n | xargs -I {} mkdir "$srcdir/program/{}"
# Copy files
find "$srcdir"/src -type f -name "*.py"  -printf %P\\n | xargs -I {} cp "$srcdir"/src/{} "$srcdir"/program/{}
find "$srcdir"/src -type f -name "*.cfg"  -printf %P\\n | xargs -I {} cp "$srcdir"/src/{} "$srcdir"/program/{}
find "$srcdir"/src -type f -name "*.cfg.sample"  -printf %P\\n | xargs -I {} cp "$srcdir"/src/{} "$srcdir"/program/{}
find "$srcdir"/src -type f -name "*.html"  -printf %P\\n | xargs -I {} cp "$srcdir"/src/{} "$srcdir"/program/{}
find "$srcdir"/src -type f -name "*.css"  -printf %P\\n | xargs -I {} cp "$srcdir"/src/{} "$srcdir"/program/{}
find "$srcdir"/src -type f -name "*.js"  -printf %P\\n | xargs -I {} cp "$srcdir"/src/{} "$srcdir"/program/{}
cd $cwd

# Add all src subdirectories to python path (This emulates the flat heirarch that 
# will exist when this script is run in Tigris
path="$PYTHONPATH":"$cwd/program"

PYTHONPATH="$path" python src/main.py -programDir $cwd -workingDir $cwd/test/output -userId=' ' -is_test=1 -file0 "$cwd/test/dataset_pred.json"



