#!/bin/bash

set
TIMESHORT=5
TIMELONG=10
BBBNUMBERROOMS=1
BBBNUMBERUSERS=1
ADMIN_WEIGHT=1
TEACHER_WEIGHT=1
PUPIL_WEIGHT=1
ANONYMOUS_WEIGHT=1
source ../loadtest_secrets.env

HOST=https://agmonlog-1.hpi-schul-cloud.dev
USER=4
TIME=10s
LOGLEVEL=INFO

pip install locust -q
PYTHONPATH=src locust -f src/loadtests/loadtests/locustfile.py -H $HOST -u $USER -t $TIME --headless -L $LOGLEVEL --only-summary
