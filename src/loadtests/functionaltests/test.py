
from loadtests.functionaltests.functionalTester import FunctionalTester


if __name__ == '__main__':
    tester = FunctionalTester('https://agmonlog-1.hpi-schul-cloud.dev')
    tester.run()
