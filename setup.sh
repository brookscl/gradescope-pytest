#!/usr/bin/env bash
apt-get update
apt-get install -y python3.8 python3.8-dev
python3.8 -m pip install -r /autograder/source/requirements.txt
