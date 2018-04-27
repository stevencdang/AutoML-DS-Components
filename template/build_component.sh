#!/bin/bash

# Author: Steven C. Dang

# This script will generate a new component
# This script assumes it is being run in the same directory as runWCC.sh
#
# Two optional arguments
#   1. the path to the directory that contains the WorkflowComponents/Templates, CommonLibraries directories
#       and the runWCC.sh script [default is cwd]
#   2. The name of the properties file that the runWCC consumes

# Write all echo statements to gen_component.log
dir=$(pwd)
LOG_FILE="$dir"/gen_component.log
exec 3>&1 1>>${LOG_FILE} 2>&1

# Handle help request
if [ "$1" == "--help" ]; then
    echo "Usage: build_component.sh [path_to_parent_of_runWCC.sh] [propFile]"
    exit 0
fi

# Handle the path argument to the runWCC.sh
if [ "$#" -gt 0 ]; then
    if [ ! "$1" == '.' ]; then
        if [[ "$1" = /* ]]; then
            dir="$1"
        else
            dir="$(pwd)"/${1%/}
        fi
    fi
fi

# Check that runWCC.sh is in the directory provided
if [ ! -d "$dir" ]; then
    echo "ERROR: Invalid directory given $dir"
    exit 1
else
    cwd=$(pwd)
    cd "$dir"
    if [ ! -f runWCC.sh ]; then
        echo "ERROR: Invalid directory given. Must provide directory that contains runWCC.sh" 1>&2
        echo "Path: $dir" 1>&2
        cd "$cwd"
        exit 1
    else
        echo "WorkflowComponents project directory is: $dir"
        cd "$cwd"
    fi
fi

# Handle the argument specifying where the wcc.properties file is
wcc=$(pwd)/wcc.properties

if [ "$#" -gt 1 ]; then
    if [[ "$2" = /* ]]; then
        wcc="$2"
    else
        wcc="$(pwd)/$2"
    fi
fi

if [ ! -f "$wcc" ]; then
    echo "ERROR: Could not find wcc.properties file at $wcc"
    exit 1
else
    echo "Running using properties file: $wcc"
fi

### Perform pre generation actions ###
#######################################
srcdir=$(dirname "$wcc")
echo "Packaging python source to be built into 'program' directory: $srcdir/program"
if [ ! -d "$srcdir"/program ]; then
    mkdir "$srcdir"/program
else
    # Clean out the old source before continuing
    rm -R "$srcdir"/program
    mkdir "$srcdir"/program
fi

# Copy all source files to the "program" folder for runWCC.sh to copy into new component folder
find "$srcdir"/src -name "*.py"  -print0 | xargs -0 cp -t "$srcdir"/program
find "$srcdir"/src -name "*.cfg"  -print0 | xargs -0 cp -t "$srcdir"/program
find "$srcdir"/src -name "*.cfg.sample" -print0 | xargs -0 cp -t "$srcdir"/program


### Generating new component ###
################################
# Ensure changing to workflow components directory so script writes out to this directory
cd $dir

# double check that the script is available
if [ ! -f runWCC.sh ]; then
    echo "ERROR: either the cwd or the first argument must be a directory that contains runWCC.sh" 1>&2
    exit 1
else
    echo "Beginning component generation"
fi

# Generate the component
# ./runWCC.sh $dir $wcc
echo "Completed component generation"

### Perform post generation actions ###
#######################################
# Get new Component name from wcc file
echo "getting Component name from $wcc"
export IFS="="
while read -r k v; do
    [ "$k" == "component.name" ] && cname=$v
done < $wcc
cdir="$dir/$cname"

# Copy component setup scripts to new component directory
cp "$srcdir"/install_component.sh "$cdir"/
cp "$srcdir"/README.md "$cdir"/ 
cp "$srcdir"/requirements.txt "$cdir"/
cp "$srcdir"/add_component.sql "$cdir"/
# mv "$cdir"/build.properties "$cdir"/build.properties.sample
echo "Copied setup files to new component directory from source directory"

# Executing install script to setup local env including new build.properties
cd "$cdir"
# ./install_component.sh
echo "Ran install script"

# Altering auto generated Java (This will vary for each component) #
####################################################################
# Getting path to java
for file in $(find "$cdir"/source -name "*.java"); do
    echo $file
    # Adding line to expose metadata to downstream components
    awk '/The addMetaData/{print $0 RS "\t\tthis.addMetaData(\"d3m-dataset\", 0, META_DATA_LABEL, \"label0\", 0, null);" RS;next}1' "$file" > tmp && mv tmp "$file"
done

# Return to current working directory after completion
cd "$cwd"
