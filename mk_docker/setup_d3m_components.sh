#!/bin/bash


# Set d3m components directory if given
if [ "$#" == "1" ]; then
    dir=$1
    cd $dir
else
    # Default working directory is parent of current dir
    cd ..
    dir=$(pwd)
fi


#rm -f ${dir}/build_errors.txt ${dir}/build_errors_info.txt
#rm -Rf */dist

echo "Current working dir: " $dir

wcc=$WCC

if [ "$wcc" == '' ]; then
    echo "WCC variable not set, using /datashop/workflow_components"
    wcc='/datashop/workflow_components'
    # Set env var for use by build_component.sh 
    export WCC=$wcc
fi

echo "Workflow components dir: " $wcc

# Find all components looking for build scripts and run the scripts
for buildfile in $(find $dir -name "build_component.sh"); do
    cdir=$(dirname $buildfile)
    ccomp=$(basename $cdir)
    if [ "$ccomp" -ne "visualizationconfusionmatrix" ]; then
        echo "Processing build file from " $ccomp
        cd $cdir
        # Create local copy of settings file if it does not exist
        if [ ! -f "src/settings.cfg" ]; then
            echo "No Settings file found. Copying from sample"
            cp src/settings.cfg.sample src/settings.cfg
        fi
        ./build_component.sh $wcc wcc.properties.template
    fi
done
#for cdir in `find $dir -maxdepth 1  -type d -name "[^.]*"`; do
  #if [ "$cdir" == "$dir/Templates" ]
  #then
    #echo "Skipping Templates dir"
    #continue
  #fi
  #cd $cdir

  #if [ -f build.xml ] && [ "$cdir" != "$dir" ]; then
    #buildOutput=`ant dist 2>> ${dir}/build_errors.txt`
    #if [ "$?" != 0 ]; then
      #echo ""
      #echo "******************************************"
      #echo "Error building jar in ${cdir}"
      #echo "******************************************"
      #echo ""
      #echo ${buildOutput} >> build_errors_info.txt
    #else
      #echo "Success: ${cdir}"
    #fi
  #fi

  #cd $dir
#done

#rm -Rf */test/ComponentTestOutput */WorkflowComponent.log */build

#if [ -s ${dir}/build_errors.txt ]; then
   ## the file is empty
   #rm ${dir}/build_errors.txt ${dir}/build_errors_info.txt
#else
   #echo "Errors were found during the build process. Please see build_errors.txt or build_errors_info.txt for additional details."
#fi



