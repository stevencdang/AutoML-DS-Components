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

# Ensure current working directory is the base directory of the component
#if [ $(basename $(pwd)) == "build_components" ]; then
    #echo "Current directory is build directory. Changing to parent to run script"
    
    #cwd="$(dirname $(pwd))"
    #cd $cwd
#else 
    #if [ ! -d "build_components" ]; then
        #echo "Current directory is not base directory of components. Please run from base directory" 1>&2
        #exit 1
    #fi
#fi

LOG_FILE="$dir"/gen_component.log
# Remove the log file if it exists
if [ -f "$LOG_FILE" ]; then
    rm $LOG_FILE
fi
echo "Writing log of output to: " $LOG_FILE
exec 3>&1 1>>${LOG_FILE} 2>&1

# Handle help request
if [ "$1" == "--help" ]; then
    echo "Usage: build_component.sh [path_to_parent_of_runWCC.sh] [propFile]" 1>&3
    exit 1
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
    echo "ERROR: Invalid directory given $dir" 1>&3
    exit 1
else
    cwd=$(pwd)
    cd "$dir"
    if [ ! -f runWCC.sh ]; then
        echo "ERROR: Invalid directory given. Must provide directory that contains runWCC.sh" 1>&3
        echo "Path: $dir" 1>&3
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

# Set current working directory to parent of wcc.propoperties
if [ "$#" -gt 1 ]; then
    if [[ "$2" = /* ]]; then
        wcctemp="$(realpath $2)"
        cwd=$(dirname $(realpath $wcctemp))
        cd $cwd
    else
        wcctemp="$(pwd)/$2"
    fi
fi


# Generate wcc from wcc template
wccdir=$(realpath $(dirname "$wcctemp"))
echo "Component Directory: " $wccdir
wcc=$wccdir/wcc.properties
awk -v cdir="$cwd" '/component.program.dir=/{print "component.program.dir=" cdir "/program";next}1' "$wcctemp" > tmp && mv tmp "$wcc"

if [ ! -f "$wcctemp" ]; then
    echo "ERROR: Could not find wcc.properties file at $wcc"
    exit 1
else
    echo "Running using properties file: " $wcc
fi
# get the location of the build component directory assuming in the component directory
build_dir="$(dirname $wccdir)/build_components"

# Get component name
tmp=$IFS
export IFS="="
while read -r k v; do
    [ "$k" == "component.name" ] && cname=$v
    [ "$k" == "component.user.name" ] && cusername=$v
    [ "$k" == "component.type" ] && ctype=$v
    [ "$k" == "component.description" ] && cdesc=$v
done < $wccdir/component.properties
echo $cname
echo $cusername
echo $cdesc
# Restore default system delmiter
export IFS=$tmp

### Perform pre generation actions ###
#######################################
# Copy all source files to the "program" folder for runWCC.sh to copy into new component folder
cd $wccdir
$build_dir/setup_run.sh

### Generating new component ###
################################
# Ensure changing to workflow components directory so script writes out to this directory
cd $dir

# double check that the script is available
if [ ! -f runWCC.sh ]; then
    echo "ERROR: either the cwd or the first argument must be a directory that contains runWCC.sh" 1>&3
    exit 1
else
    echo "Beginning component generation"
fi

# Setup path to new workflow component directory
cdir="$dir/$cname"
if [ -d "$cdir" ]; then
    echo "######################################" 1>&3
    echo "Found existing generated workflow component: " $cdir 1>&3
    echo "Deleting before generating"  1>&3
    # rm -Rf "$cdir"
fi
# Generate the component
./runWCC.sh $dir $wcc
echo "Completed component generation"

### Perform post generation actions ###
#######################################

# Copy component setup scripts to new component directory
srcdir=$(dirname "$wcc")
cp "$build_dir"/install_component.sh "$cdir"/
cp "$build_dir"/README.md "$cdir"/ 
cp "$build_dir"/requirements.txt "$cdir"/
cp "$build_dir"/.gitignore.component "$cdir"/.gitignore
# Copy sql component script generator with custom component fields
cp "$build_dir"/gen_add_component.sh "$cdir"/
file="gen_add_component.sh"
awk -v cname=$cname '/comp_dir_name=/{print "comp_dir_name=\"" cname "\"";next}1' "$file" > tmp && mv tmp "$file"
awk -v cusername="$cusername" '/comp_user_name/{str = $0; gsub("comp_user_name", cusername, str); print str;next}1' "$file" > tmp && mv tmp "$file"
awk -v cvar="$ctype" '/comp_type/{str = $0; gsub("comp_type", cvar, str); print str;next}1' "$file" > tmp && mv tmp "$file"
awk -v cvar="$ctype" '/comp_desc/{str = $0; gsub("comp_desc", cvar, str); print str;next}1' "$file" > tmp && mv tmp "$file"

cp "$srcdir"/build.xml "$cdir"/
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
    #awk '/The addMetaData/{print $0 RS "\t\tthis.addMetaData(\"d3m-dataset\", 0, META_DATA_LABEL, \"label0\", 0, null);" RS;next}1' "$file" > tmp && mv tmp "$file"
done

# Altering auto generated test xml (This will vary for each component) #
########################################################################
for file in $(find "$cdir"/test/components -name "*.xml"); do
    echo "Editing test xml: " $file
    # Inserting path to test file into test xml
    # awk -v cdir="$cdir" '/<file_path>/{print "<file_path>" cdir "/test/components/datasetDoc.tsv</file_path>";next}1' "$file" > tmp && mv tmp "$file"
    # Inserting name of test file into test xml
    # awk -v cdir="$cdir" '/<file_name>/{print "<file_name>datasetDoc.tsv</file_name>";next}1' "$file" > tmp && mv tmp "$file"
done

# Run a test of the component using ant #
#########################################
#echo "Running 'ant runComponent' to test the component install"
#`ant runComponent`

# Cleanup autogenerated file
echo "Clearning up wcc.properties generated file: " $wcc
rm $wcc

# Return to current working directory after completion
echo "Returning to original directory: " $cwd
cd "$cwd"
echo "Make sure to look at " $cdir"/program/settings.cfg to ensure all settings are correct for the local machine" 1>&3
echo "Build component completed"
