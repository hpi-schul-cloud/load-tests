#! /usr/bin/env bash
export FUNCTIONAL_TEST=1
export TARGET_URL=https://infra.schulcloud-02.dbildungscloud.dev

pip install -r requirements.txt -q
PYTHONPATH=src:$PYTHONPATH python3 src/loadtests/functionaltests/main.py
