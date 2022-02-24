
from loadtests.functionaltests.functionalTester import FunctionalTester


if __name__ == '__main__':
    #host = 'https://agmonlog-1.hpi-schul-cloud.dev'
    host = 'https://staging.niedersachsen.dbildungscloud.org'
    tester = FunctionalTester(host)
    tester.run()
