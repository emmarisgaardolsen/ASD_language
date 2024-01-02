#!/bin/bash

# create virtual envrionment
python -m venv child_env

source ./child_env/bin/activate

# install requirements
python -m pip install -r requirements.txt

# deactivate env
deactivate