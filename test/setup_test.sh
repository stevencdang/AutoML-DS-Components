#!/bin/bash

# This script will run all the components in a simple test setup. Can be used 
# to configure the directory after a fresh pull

if [ -z ${D3MCONFIG+x} ]; then 
    echo "D3MCONFIG not set. setting to:" $WCC"/D3M/d3m.cfg"
    export D3MCONFIG=$WCC/D3M/d3m.cfg
fi


# Go through each module and configure it to run
cd ..
cwd=$(pwd)
for f in $(find . -name "build_component.sh"); do
    full_path=$(realpath $f)
    dir=$(dirname $full_path)
    echo "Found component" $dir
    cd $dir 
    # Run configuration scripts
    if [ ! -f src/settings.cfg ]; then
        echo "No settings.cfg file found. Copying from sample"
        cp src/settings.cfg.sample src/settings.cfg
    fi
    ./setup_test.sh 
    cd $cwd
done

