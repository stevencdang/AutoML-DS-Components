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

## Cloning instructions
This project includes a number of submodules for each workflow component. In order to clone the project to your local 
machine, you have to perform the following commands

```
git clone <repo_addr>
git submodule init
git submodule update
```

Alternatively you can clone with all submodules in one command:

```
git clone  --recurse-submodules <repo_address>
```

# Setting up local Git environment for convenience

To work with submodules conveniently, it is usefule to alias a few submodule commands so it is cleaner to operate on 
all submodules.

```
# Update and merge remote changes into local submodules
git config alias.supdate 'submodule update --remote --merge'
git config alias.spush 'push --recurse-submodules=on-demand'

# 
```

In order to make modifications to the submodule you should execute the following commands after cloning. This will put 
each local clone of each submodule on its own branch.

```
git submodule forech 'git branch dev'
git submodule forech 'git checkout dev'
```
