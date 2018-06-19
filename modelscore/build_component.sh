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
# Remove the log file if it exists
if [ -f "$LOG_FILE" ]; then
    rm $LOG_FILE
fi
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
            # hack to resolve if relative path is given with ../..
            cwd="$(pwd)"
            cd "$dir"
            dir="$(pwd)"
            cd "$cwd"
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
wcctemp=$(pwd)/wcc.properties.template
#wccdir=$(pwd)

if [ "$#" -gt 1 ]; then
    if [[ "$2" = /* ]]; then
        wcctemp="$2"
    else
        wcctemp="$(pwd)/$2"
    fi
fi

if [ ! -f "$wcctemp" ]; then
    echo "ERROR: Could not find wcc.properties file at $wcc"
    exit 1
else
    echo "Running using properties file: $wcc"
fi

# Generate wcc from wcc template
wccdir=$(dirname "$wcctemp")
wcc=$wccdir/wcc.properties
awk -v cdir="$cwd" '/component.program.dir=/{print "component.program.dir=" cdir "/program";next}1' "$wcctemp" > tmp && mv tmp "$wcc"


### Perform pre generation actions ###
#######################################
#srcdir=$(dirname "$wcc")
#echo "Packaging python source to be built into 'program' directory: $srcdir/program"
#if [ ! -d "$srcdir"/program ]; then
    #mkdir "$srcdir"/program
#else
    ## Clean out the old source before continuing
    #rm -R "$srcdir"/program
    #mkdir "$srcdir"/program
#fi

# Copy all source files to the "program" folder for runWCC.sh to copy into new component folder
./setup_run.sh

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
./runWCC.sh $dir $wcc
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
srcdir=$(dirname "$wcc")
cp "$srcdir"/install_component.sh "$cdir"/
cp "$srcdir"/README.md "$cdir"/ 
cp "$srcdir"/requirements.txt "$cdir"/
cp "$srcdir"/gen_add_component.sh "$cdir"/
cp "$srcdir"/.gitignore.component "$cdir"/.gitignore
#mv "$cdir"/build.properties "$cdir"/build.properties.sample
cp "$srcdir"/test/datasetDoc.tsv "$cdir"/test/components/
cp "$srcdir"/test/problemDoc.tsv "$cdir"/test/components/
echo "Copied setup files to new component directory from source directory"

# Create dir for writing logs
mkdir "$cdir"/logs
# Set log directory in the settings
for file in $(find "$cdir"/program -name "settings.cfg"); do
    awk -v cdir=$cdir '/file_log_path/{print "file_log_path = " cdir "/logs";next}1' "$file" > tmp && mv tmp "$file"
done


# Create build.properties.sample
echo "component.interpreter.path=/usr/local/bin/python" > "$cdir"/build.properties.sample
echo "component.program.path=program/main.py" >> "$cdir"/build.properties.sample

# Executing install script to setup local env including new build.properties
cd "$cdir"
./install_component.sh
echo "Ran install script"

# Altering auto generated Java (This will vary for each component) #
####################################################################
# Getting path to java
for file in $(find "$cdir"/source -name "*.java"); do
    echo "Editing java file: " $file
    # Adding line to expose metadata to downstream components
    awk '/The addMetaData/{print $0 RS "\t\tthis.addMetaData(\"d3m-dataset\", 0, META_DATA_LABEL, \"label0\", 0, null);" RS;next}1' "$file" > tmp && mv tmp "$file"
done

# Altering auto generated test xml (This will vary for each component) #
########################################################################
for file in $(find "$cdir"/test/components -name "*.xml"); do
    echo "Editing test xml: " $file
    # Inserting path to test file into test xml
    awk -v cdir="$cdir" '/<file_path>/{print "<file_path>" cdir "/test/components/datasetDoc.tsv</file_path>";next}1' "$file" > tmp && mv tmp "$file"
    # Inserting name of test file into test xml
    awk -v cdir="$cdir" '/<file_name>/{print "<file_name>datasetDoc.tsv</file_name>";next}1' "$file" > tmp && mv tmp "$file"
done

# Run a test of the component using ant #
#########################################
#echo "Running 'ant runComponent' to test the component install"
#`ant runComponent`

# Cleanup autogenerated file
rm $wcc
# Return to current working directory after completion
cd "$cwd"
echo "Make sure to look at <ComponentDir>/program/settings.cfg to ensure all settings are correct for the local machine" 1>&3
echo "Build component completed"
