#!/bin/bash

export TIMESHORT=5
export TIMELONG=10
export BBBNUMBERROOMS=1
export BBBNUMBERUSERS=1
export ADMIN_WEIGHT=1
export TEACHER_WEIGHT=1
export PUPIL_WEIGHT=1
export ANONYMOUS_WEIGHT=1
export FUNCTIONAL_TEST=0

HOST=https://agmonlog-1.hpi-schul-cloud.dev
USER=4
TIME=10s
LOGLEVEL=INFO

pip install -r requirements.txt -q
PYTHONPATH=src locust -f src/loadtests/loadtests/locustfile.py -H $HOST -u $USER -t $TIME --headless -L $LOGLEVEL --only-summary
