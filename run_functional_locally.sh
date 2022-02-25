
export TIMESHORT=5
export TIMELONG=10
export BBBNUMBERROOMS=1
export BBBNUMBERUSERS=1
export ADMIN_WEIGHT=1
export TEACHER_WEIGHT=1
export PUPIL_WEIGHT=1
export ANONYMOUS_WEIGHT=1

pip install -r requirements.txt -q
PYTHONPATH=src python src/loadtests/functionaltests/test.py
