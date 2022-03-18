
export TIMESHORT=5
export TIMELONG=10
export FUNCTIONAL_TEST=1

pip install -r requirements.txt -q
PYTHONPATH=src python src/loadtests/functionaltests/test.py
