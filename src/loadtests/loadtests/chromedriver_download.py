import logging
import os
import pyderman as driver

URL = 'https://chromedriver.storage.googleapis.com/'
FALLBACK_URL = 'https://chromedriver.storage.googleapis.com/100.0.4896.20/chromedriver_linux64.zip'
WORKSPACE = os.path.dirname(os.path.abspath(__file__))

def asure_chromedriver():
    if not os.path.isfile(os.path.join(WORKSPACE, 'chromedriver')):
        download_chromedriver()

def download_chromedriver():
    path = driver.install(browser=driver.chrome, file_directory=WORKSPACE,filename='chromedriver')
    print('Installed chromdriver driver to path: %s' % path)

if __name__ == '__main__':
    download_chromedriver()
