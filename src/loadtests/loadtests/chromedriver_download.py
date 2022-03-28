import logging
import os
import stat
import zipfile
from io import BytesIO
from typing import Tuple, List, Any

import requests
from defusedxml import ElementTree


URL = 'https://chromedriver.storage.googleapis.com/'
FALLBACK_URL = 'https://chromedriver.storage.googleapis.com/100.0.4896.20/chromedriver_linux64.zip'
WORKSPACE = os.path.dirname(os.path.abspath(__file__))


def asure_chromedriver():
    if not os.path.isfile(os.path.join(WORKSPACE, 'chromedriver')):
        download_chromedriver()


def download_chromedriver():
    if not URL.startswith('https://') or not FALLBACK_URL.startswith('https://'):
        raise RuntimeError(f'Won\'t do automatic downloads from {URL} or {FALLBACK_URL} (no HTTPS)')
    response = requests.get(URL)
    response.raise_for_status()
    try:
        bucket = ElementTree.fromstring(response.text)
        contents = [content for content in bucket if content.tag.endswith('Contents')]
        url = get_latest_version_url(contents)
    except (ValueError, RuntimeError):
        logging.warning('using fallback url for chromedriver download')
        url = FALLBACK_URL
    response = requests.get(URL + url)
    response.raise_for_status()
    zip = zipfile.ZipFile(BytesIO(response.content), 'r')
    zip.extractall(WORKSPACE)
    os.chmod(os.path.join(WORKSPACE, 'chromedriver'), stat.S_IRWXU)
    zip.close()


def get_latest_version_url(contents_list: List[Any]):
    max_version = (0, 0, 0, 0)
    max_url = ''
    for content in contents_list:
        for child in content:
            if child.tag.endswith('Key') and child.text.endswith('linux64.zip'):
                version = child.text.split('/')[0].split('.')
                if higher(version, max_version):
                    max_version = version
                    max_url = child.text
    if not max_url:
        raise RuntimeError('Could not find satisfying chromedriver download')
    return max_url


def higher(version1: Tuple[int], version2: Tuple[int]):
    n = min(len(version1), len(version2))
    for i in range(n):
        try:
            a, b = int(version1[i]), int(version2[i])
            if a < b:
                return False
            elif a > b:
                return True
        except ValueError:
            return False
    if len(version1) > len(version2):
        return True
    return False


if __name__ == '__main__':
    download_chromedriver()
