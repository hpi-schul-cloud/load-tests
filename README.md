# HPI SchulCloud load tests

To test the performance of the HPI-SchulCloud application, multiple useres will be simulated by the loadtest. It creates a provided number of users, which are different by their user-type (admin, techer, pupil), and swarms the system simultaneausly, simulating their behavior. Courses, BBB-rooms, tasks etc. will be created, edited and deleted to generate additional traffic, and is captured on the Locust web-interface for subsequent analysis.
Actually the loadtest implementation provides two kinds of starting the tests:
- scalable load tests which are designed to run with a specified number of user from the locust web interface
- functional tests which do not scale but execute the same tests as the load tests, this startup typ could be used for smoke testing a fresh deployed instance or regular verfying the proper funtion of a running instance
The functional tests provide the number of executed and failed tests as Prometheus metrics to allow alerting on failed tests.
## Requirements

- Python (>= 3.6.10)
- ChromeDriver (>= 90.0.4430.24, just necessary for BBB-Loadtest, Document-Loadtest)
- Docker (>= 19.03.5, optional)

## Preparations

1. Download ChromeDriver
- The chromedriver.exe needs to be in the same path as the locustfile.py-File
2. Configure the environment (config.py, launch.json)
- Shared Variables
  * PYTHONPATH=./src:${PYTHONPATH}
  * ADMIN_EMAIL=admin@schul-cloud.org
  * ADMIN_PASSWORD=<admin_password>
  * TEACHER_EMAIL=lehrer@schul-cloud.org
  * TEACHER_PASSWORD=<teacher_password>
  * PUPIL_EMAIL=schueler@schul-cloud.org
  * PUPIL_PASSWORD=<pupil_password>
  * ANONYMOUS_EMAIL=hugo@dbildungscloud.de
  * ANONYMOUS_PASSWORD=<anonymous_password>
  * BBB_ROOM_COUNT            : INT of Rooms of BBB
  * BBB_USER_COUNT            : INT of Users per Room
  * WEIGHT_ADMIN              : INT users weight
  * WEIGHT_TEACHER            : INT users weight
  * WEIGHT_PUPIL              : INT users weight
  * WEIGHT_ANONYMOUS          : INT users weight
  * WEIGHT_ACTUAL_ANONYMOUS   : INT users weight
  * WEIGHT_EXTERNAL_PUPIL     : INT users weight
  * WAIT_TIME_SHORT           : Time in Sec
  * WAIT_TIME_LONG            : Time in Sec
- Load Test specific Variables
  * FUNCTIONAL_TEST : 0  
  * LOADTEST_EXTERNAL: 0 / 1  : Test IDM with schulcloud-server
- Functional Test specific Variables
  * FUNCTIONAL_TEST : 1  
  * TARGET_URL      : Specify the instance to be tested as FQDN, e.g. https://nidersachsen.cloud
  * Optional: 
    * TIMEINTERVAL_SEC : Time in sec to sleep between repeated tests, default is 300
    * PROMETHEUS_PORT port to expose Prometheus metrics, default is 9000
1. Install required programs with `pip3 install -r requirements.txt`

## Run the load tests locally

Load tests make use of selenium with remote browser. To mimic this locally setup the following:

1. Download selenium server from https://www.selenium.dev/downloads/
1. Follow the setup steps for selenium server according to https://www.selenium.dev/documentation/grid/getting_started/
1. Set the `BROWSERIPPORT` environment variable to match with your local selenium server (i.e. 'localhost:4444')
1. Start the server with the following command:
```
 `java -jar selenium-server-<version>.jar standalone`
 ```
### Command line and web-interface
To run the load test, first open a command line and start locust with the following command:
```
`locust -f ./locustfile.py --host https://hackathon.hpi-schul-cloud.de --tags test`
```
Insert the right host after the '--host' tag*
*  The '--tags test' tag is optional and will only start tasks which are marked with this tag*

Afterwards, start your webbrowser and open `localhost:8089` or `http://127.0.0.1:8089/`. The locust web-interface should load, and you can fill out the form and start swarming. \
For further information about running locust check out their [documentation](https://docs.locust.io/en/stable/quickstart.html#start-locust).

### Docker

```
docker run -it --rm --entrypoint /bin/sh -v "$(pwd)":/app -w /app locustio/locust:0.14.4
pip install -r requirements.txt
locust -f ./locustfile.py --no-web --clients 20 --run-time 30s --host https://hackathon.hpi-schul-cloud.de --logfile $(date '+%Y-%m-%d-%H:%M:%S')-hackathon.log --csv=$(date '+%Y-%m-%d-%H:%M:%S')-hackathon
```

## Run the functional tests locally
Execute the following command at the top level of the repository
```
python3 src/loadtests/functionaltests/main.py
```
