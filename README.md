# HPI Schul-Cloud load tests

Running load tests for HPI Schul-Cloud application, which swarms the system witch multiple simultaneous users and simulates their behavior.

## Requirements

- Python (>= 3.6.10)
- ChromeDriver (>= 90.0.4430.24, just necessary for BBB-Loadtest, Document-Loadtest)
- Docker (>= 19.03.5, optional)

## Preparations

1. Download ChromeDriver
  - The chromedriver.exe needs to be in the same path as the locustfile.py-File
2. Create a YAML file with user credentials (email, password)
  - Filename should be `users_${HOSTNAME}.yaml`.

Example for `HOSTNAME=hackathon.hpi-schul-cloud.de`:
```
# file: users_hackathon.hpi-schul-cloud.de.yaml
---
admin:
  - email: admin@schul-cloud.org
    password: foo
teacher:
  - email: lehrer@schul-cloud.org
    password: bar
pupil:
  - email: schueler@schul-cloud.org
    password: baz
```
3. Install required programs with `pip3 install -r requirements.txt`
4. Create new environment variables to finish the config:
```
BBBKEY          : Key for BigBlueButton
BBBHOST         : URL of BigBlueButton
BBBNUMBERROOMS  : INT of Rooms of BBB
BBBNUMERUSERS   : INT of Users per Room
MMHOST          : URL of MatrixMessenger
TIMESHORT       : Time in Sec
TIMELONG        : Time in Sec
```

## Run the load tests

### Command line and web-interface
To run the load test, first open a command line and start locust with the following command: \
`locust -f ./locustfile.py --host https://hackathon.hpi-schul-cloud.de --tags test`

*- Insert the right host after the '--host' tag* \
*- The '--tags test' tag is optional and will only start tasks which are marked with this tag*

Afterwards, start your webbrowser and open `localhost:8089` or `http://127.0.0.1:8089/`. The locust web-interface should load, and you can fill out the form and start swarming. \
For further informations about running locust check out their [documentation](https://docs.locust.io/en/stable/quickstart.html#start-locust).

### Docker

```
docker run -it --rm --entrypoint /bin/sh -v "$(pwd)":/app -w /app locustio/locust:0.14.4
pip install -r requirements.txt
locust -f ./locustfile.py --no-web --clients 20 --run-time 30s --host https://hackathon.hpi-schul-cloud.de --logfile $(date '+%Y-%m-%d-%H:%M:%S')-hackathon.log --csv=$(date '+%Y-%m-%d-%H:%M:%S')-hackathon
```
