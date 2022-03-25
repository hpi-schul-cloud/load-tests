
export FUNCTIONAL_TEST=1

pip install -r requirements.txt -q
PYTHONPATH=src python3 src/loadtests/functionaltests/main.py
