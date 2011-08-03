#!/bin/sh
#
# Boostrap the Python virtual environment
VIRTUALENV=./ve
virtualenv --no-site-packages --distribute "$VIRTUALENV"
source ve/bin/activate
easy_install pip
pip install -r pip-requirements.txt && \
echo "A python virtual environment has been set up in $VIRTUALENV"
echo "Type this command to activate the virtual environment:"
echo " source ve/bin/activate"
