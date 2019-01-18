#!/bin/bash
# Carnegie Mellon University, Human-Computer Interaction Institute.
# Copyright 2018. All Rights Reserved.
#
# Purpose: Sets up the initial Docker directory with the Dockerfile
# Requires: Docker -- see Docker setup instructions in
# DON'T run as root
whoami=`whoami`
if [ "$whoami" == "root" ]; then
  echo "Will not run as root."
  exit
fi

read -p "SVN User: " MYUSER
read -s -p "SVN Password: " MYPWD
echo ""
read -p "Bitbucket User: " BBUSR
read -s -p "Bitbucket Password: " BBPWD
echo ""

CWD=$(pwd)
DS_DIRECTORY="$CWD"/DataShopDocker

mkdir -p  $DS_DIRECTORY

if [ ! -d "${DS_DIRECTORY}/tools" ]; then
        svn --password ${MYPWD} --username ${MYUSER} co svn://pact-cvs.pact.cs.cmu.edu/usr4/local/DataShopSvnRoot/DataShopAdmin/trunk/tools $DS_DIRECTORY/tools
        svn_success_status=`echo $?`
        cd ${DS_DIRECTORY}/tools
        svn --password ${MYPWD} --username ${MYUSER} cleanup
        svn --password ${MYPWD} --username ${MYUSER} update
        svn_success_status=`echo $?`
else
        cd ${DS_DIRECTORY}/tools
        svn --password ${MYPWD} --username ${MYUSER} cleanup
        svn --password ${MYPWD} --username ${MYUSER} update
        svn_success_status=`echo $?`
fi

if [ "$svn_success_status" == "0" ] && [ ! -d "${DS_DIRECTORY}/deploy" ]; then
        svn --password ${MYPWD} --username ${MYUSER} co --depth files svn://pact-cvs.pact.cs.cmu.edu/usr4/local/DataShopSvnRoot/DataShopAdmin/tags/DATASHOP_10_1_10_patch/deploy $DS_DIRECTORY/deploy
        svn_success_status=`echo $?`
        cd ${DS_DIRECTORY}/deploy
        svn --password ${MYPWD} --username ${MYUSER} cleanup
        svn --password ${MYPWD} --username ${MYUSER} update
        svn_success_status=`echo $?`
elif [ "$svn_success_status" == "0" ]; then
        cd ${DS_DIRECTORY}/deploy
        svn --password ${MYPWD} --username ${MYUSER} cleanup
        svn --password ${MYPWD} --username ${MYUSER} update
        svn_success_status=`echo $?`
else
        echo "SVN failed."
        exit
fi

# Add the SemanticSpace folder containing TASA1 to your home if it exists ( ~/SemanticSpace/ can be obtained by contacting datashop)
if [ -d ~/SemanticSpace/ ]; then
  cp -R ~/SemanticSpace/ ${DS_DIRECTORY}
fi

if [ "$svn_success_status" == "0" ] && [ ! -d "${DS_DIRECTORY}/deploy/vm" ]; then
        svn --password ${MYPWD} --username ${MYUSER} co --depth files svn://pact-cvs.pact.cs.cmu.edu/usr4/local/DataShopSvnRoot/DataShopAdmin/tags/DATASHOP_10_1_10_patch/deploy/vm $DS_DIRECTORY/deploy/vm
        svn_success_status=`echo $?`
        cd ${DS_DIRECTORY}/deploy/vm
        svn --password ${MYPWD} --username ${MYUSER} cleanup
        svn --password ${MYPWD} --username ${MYUSER} update
        svn_success_status=`echo $?`
elif [ "$svn_success_status" == "0" ]; then
        cd ${DS_DIRECTORY}/deploy/vm
        svn --password ${MYPWD} --username ${MYUSER} cleanup
        svn --password ${MYPWD} --username ${MYUSER} update
        svn_success_status=`echo $?`
else
        echo "SVN failed."
        exit
fi

# Because of issues with svn, make sure we try a few times to update the deploy/vm directory.
if [ "$svn_success_status" != "0" ]; then
        cd ${DS_DIRECTORY}/deploy/vm
        svn --password ${MYPWD} --username ${MYUSER} cleanup
        svn --password ${MYPWD} --username ${MYUSER} update
        svn_success_status=`echo $?`
else
        echo "Successfully obtained .war file"
fi
if [ "$svn_success_status" == "0" ] && [ ! -d "${DS_DIRECTORY}/sql" ]; then
        svn --password ${MYPWD} --username ${MYUSER} co svn://pact-cvs.pact.cs.cmu.edu/usr4/local/DataShopSvnRoot/DataShop/tags/DATASHOP_10_1_10_patch/java/sql/v10.x $DS_DIRECTORY/sql
        svn_success_status=`echo $?`
        cd ${DS_DIRECTORY}/sql
        svn --password ${MYPWD} --username ${MYUSER} cleanup
        svn --password ${MYPWD} --username ${MYUSER} update
        svn_success_status=`echo $?`
elif [ "$svn_success_status" == "0" ]; then
        cd ${DS_DIRECTORY}/sql
        svn --password ${MYPWD} --username ${MYUSER} cleanup
        svn --password ${MYPWD} --username ${MYUSER} update
        svn_success_status=`echo $?`
else
        echo "SVN failed."
        exit
fi

svn --password ${MYPWD} --username ${MYUSER} export --force svn://pact-cvs.pact.cs.cmu.edu/usr4/local/DataShopSvnRoot/DataShop/tags/DATASHOP_10_1_10_patch/java/sql/create_databases.sql $DS_DIRECTORY/sql/create_databases.sql
svn --password ${MYPWD} --username ${MYUSER} export --force svn://pact-cvs.pact.cs.cmu.edu/usr4/local/DataShopSvnRoot/DataShop/tags/DATASHOP_10_1_10_patch/java/sql/create_empty_auth_db.sql $DS_DIRECTORY/sql/create_empty_auth_db.sql
svn --password ${MYPWD} --username ${MYUSER} export --force svn://pact-cvs.pact.cs.cmu.edu/usr4/local/DataShopSvnRoot/DataShop/tags/DATASHOP_10_1_10_patch/java/sql/workflow_component_local.sql $DS_DIRECTORY/sql/workflow_component_local.sql
svn --password ${MYPWD} --username ${MYUSER} export --force svn://pact-cvs.pact.cs.cmu.edu/usr4/local/DataShopSvnRoot/DataShop/tags/DATASHOP_10_1_10_patch/java/sql/workflow_error_translation.sql $DS_DIRECTORY/sql/workflow_error_translation.sql

if [ "$svn_success_status" == "0" ] && [ ! -d "${DS_DIRECTORY}/docker_datashop" ]; then
        svn --password ${MYPWD} --username ${MYUSER} co svn://pact-cvs.pact.cs.cmu.edu/usr4/local/DataShopSvnRoot/DataShopAdmin/trunk/docker_datashop $DS_DIRECTORY/docker_datashop
        svn_success_status=`echo $?`
        cd ${DS_DIRECTORY}/docker_datashop
        svn --password ${MYPWD} --username ${MYUSER} cleanup
        svn --password ${MYPWD} --username ${MYUSER} update
        svn_success_status=`echo $?`
elif [ "$svn_success_status" == "0" ]; then
        cd ${DS_DIRECTORY}/docker_datashop
        svn --password ${MYPWD} --username ${MYUSER} cleanup
        svn --password ${MYPWD} --username ${MYUSER} update
        svn_success_status=`echo $?`
else
        echo "SVN failed."
        exit
fi

if [ "$svn_success_status" == "0" ] && [ ! -d "${DS_DIRECTORY}/init" ]; then
        svn --password ${MYPWD} --username ${MYUSER} co --depth files svn://pact-cvs.pact.cs.cmu.edu/usr4/local/DataShopSvnRoot/DataShopAdmin/trunk/init $DS_DIRECTORY/init
        svn_success_status=`echo $?`
        cd ${DS_DIRECTORY}/deploy/vm
        svn --password ${MYPWD} --username ${MYUSER} cleanup
        svn --password ${MYPWD} --username ${MYUSER} update
        svn_success_status=`echo $?`
elif [ "$svn_success_status" == "0" ]; then
        cd ${DS_DIRECTORY}/deploy/vm
        svn --password ${MYPWD} --username ${MYUSER} cleanup
        svn --password ${MYPWD} --username ${MYUSER} update
        svn_success_status=`echo $?`
else
        echo "SVN failed."
        exit
fi

if [ "$svn_success_status" == "0" ] && [ ! -d "${DS_DIRECTORY}/extlib" ]; then
        svn --password ${MYPWD} --username ${MYUSER} export svn://pact-cvs.pact.cs.cmu.edu/usr4/local/DataShopSvnRoot/DataShop/tags/DATASHOP_10_1_10_patch/java/extlib $DS_DIRECTORY/extlib
        svn_success_status=`echo $?`
        cd ${DS_DIRECTORY}/extlib
        svn --password ${MYPWD} --username ${MYUSER} cleanup
        svn --password ${MYPWD} --username ${MYUSER} update
        svn_success_status=`echo $?`
elif [ "$svn_success_status" == "0" ]; then
        cd ${DS_DIRECTORY}/extlib
        svn --password ${MYPWD} --username ${MYUSER} cleanup
        svn --password ${MYPWD} --username ${MYUSER} update
        svn_success_status=`echo $?`
else
        echo "SVN failed."
        exit
fi

# Copy a public SSH key to the docker image
mkdir -p $DS_DIRECTORY/ssh && cp ~/.ssh/id_rsa.pub $DS_DIRECTORY/ssh/id_rsa.pub
#mkdir -p $DS_DIRECTORY/ssh && cp /home/tigris/.ssh/id_rsa.pub $DS_DIRECTORY/ssh/id_rsa.pub

cd $DS_DIRECTORY

#git clone --depth 1 https://github.com/LearnSphere/WorkflowComponents.git workflow_components
# Grab d3m specfic branch
git clone --depth 1 -b d3m --single-branch https://github.com/LearnSphere/WorkflowComponents.git workflow_components

# Grab d3m component code library for development
git clone https://${BBUSR}:${BBPWD}@bitbucket.org/stevencdang/learnsphere_workflow_components.git d3m_components

# Grab python 3.6 to build and install
#cd $DS_DIRECTORY
wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tar.xz  && tar xvf Python-3.6.3.tar.xz
#cd $DS_DIRECTORY

cp -R $DS_DIRECTORY/docker_datashop/* $DS_DIRECTORY/

cp $DS_DIRECTORY/docker_datashop/no-ssl-10_1_10_patch/datashop.war $DS_DIRECTORY/deploy/vm/datashop.war

#################################
# Copy Dockerfile to override standard one
cp $CWD/Dockerfile $DS_DIRECTORY/
# OVerwrive component generation script
cp $CWD/setup_d3m_components.sh $DS_DIRECTORY/d3m_components/mk_docker/ # this is only during dev
# Overwrite the docker start script
cp $CWD/start.sh $DS_DIRECTORY/start.sh
# Overwrite the sql script that adds components
cp $CWD/workflow_component_local.sql $DS_DIRECTORY/sql/
# Add a .vimrc file for development
cp $CWD/.vimrc $DS_DIRECTORY/
cp $CWD/.gitconfig $DS_DIRECTORY/

#docker stop ds_instance_alpha ; docker rm ds_instance_alpha ;
#docker build -t ds_image_alpha .
#echo "TO START THE INSTANCE: docker run -p 9001:443 -p 9000:22 --mount type=bind,source=<dataset_root>,target=/data/datasets --mount type=bind,source=<ta2_write_dir>,target=/data/output -P --name ds_instance_alpha ds_image_alpha"
#echo "TO STOP THE INSTANCE: docker stop ds_instance_alpha"
#echo "TO REMOVE THE INSTANCE: docker rm ds_instance_alpha"
#echo "TO TAG: docker tag ds_image_alpha:latest 016042509432.dkr.ecr.us-east-1.amazonaws.com/ds_image_alpha:latest"
#echo "TO PUSH TO AWS: docker push 016042509432.dkr.ecr.us-east-1.amazonaws.com/ds_image_alpha:latest"
#docker stop registry.datadrivendiscovery.org/sdang/cmu-ta3 ; docker rm registry.datadrivendiscovery.org/sdang/cmu-ta3 ;
#docker build -t registry.datadrivendiscovery.org/sdang/cmu-ta3 .
#echo "TO START THE INSTANCE: docker run -p 9000:443 -P --name registry.datadrivendiscovery.org/sdang/cmu-ta3 ds_image_alpha"
#echo "TO STOP THE INSTANCE: docker stop registry.datadrivendiscovery.org/sdang/cmu-ta3"
#echo "TO REMOVE THE INSTANCE: docker rm registry.datadrivendiscovery.org/sdang/cmu-ta3"
#echo "TO TAG: docker tag ds_image_alpha:latest 016042509432.dkr.ecr.us-east-1.amazonaws.com/ds_image_alpha:latest"
#echo "TO PUSH TO AWS: docker push 016042509432.dkr.ecr.us-east-1.amazonaws.com/ds_image_alpha:latest"

# Additional docker run args you might want to try
# -d, --detach=false         Run container in background and print container ID
# -t, --tty=false            Allocate a pseudo-TTY

