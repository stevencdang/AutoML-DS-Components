# Collection of Tigris worflow Components

Carnegie Mellon University, Massachusetts Institute of Technology, Stanford University, University of Memphis.
Copyright 2016. All Rights Reserved.

## LearnSphere and Tigris

[LearnSphere](LearnSphere.org) is co-developed by the [LearnLab](http://learnlab.org) – a flagship project of [Carnegie Mellon](http://cmu.edu)'s [Simon Initiative](https://www.cmu.edu/simon). It is community software infrastructure for sharing, analysis, and collaboration of/around educational data. LearnSphere integrates existing and new educational data infrastructures to offer a world class repository of education data. 

[Tigris](https://pslcdatashop.web.cmu.edu/LearnSphereLogin) is a workflow authoring tool which is part of the community software infrastructure being built for the LearnSphere project. The platform provides a way to create custom analyses and interact with new as well as existing data formats and repositories.

## System Dependencies
* Python 2.7
* VirtualEnv

## Component List
# D3M Components
* Dataset Selector
* Pipeline Search

## TA3 docker container deployment

# CMU TA3

## Prerequisites
1. A TA2 is running and accessible.

## Command to launch the docker image
Assuming a TA2 is running at ```localhost:45042```.

```bash
docker run -it \
    --rm \
    -p 8080:80 \
    --mount type=bind,source=<path_to_local_dataset_dir>,target=/input \
    --mount type=bind,source=<any_writable_dir>,target=/output \
    -e "D3MCONFIG=/datashop/workflow_components/D3M/d3m.cfg" \
    -e D3MINPUTDIR=/input \
    -e D3MOUTPUTDIR=/output \
    -e TA2ADDR="localhost:45042" \
    -e TA2NAME=<name_of_the_TA2> \
    registry.datadrivendiscovery.org/sdang/cmu-ta3:live
```

Example of using CMU TA2 that runs at port 45042
```bash
docker run -it \
    --rm \
    -p 8080:80 \
    --mount type=bind,source=/data/data/d3m/dryrun2018summer/input,target=/input \
    --mount type=bind,source=/data/data/d3m/dryrun2018summer/output,target=/output \
    -e "D3MCONFIG=/datashop/workflow_components/D3M/d3m.cfg" \
    -e D3MINPUTDIR=/input \
    -e D3MOUTPUTDIR=/output \
    -e TA2ADDR="localhost:45042" \
    -e TA2NAME="cmu" \
    registry.datadrivendiscovery.org/sdang/cmu-ta3:live
```

Then point your browser to [https://localhost:8080](https://localhost:8080).



