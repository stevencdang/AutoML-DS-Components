#!/bin/bash

# This script sets up a local python dev env within this folder for developing the component

# Assumed dependencies:
# -- python pip
# -- python virtualenv
echo "Setting up test env wihtin project folder for development"

virtualenv env --python=python3.6
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

mkdir test 
mkdir test/output

# Deactiate python venv
deactivate
