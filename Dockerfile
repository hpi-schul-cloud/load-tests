FROM python:3.9.12
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src ./src

CMD [ "PYTHONPATH=src:$PYTHONPATH", "python3", "src/loadtests/functionaltests/main.py"]