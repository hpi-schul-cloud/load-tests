
import sys
import os
import logging
from typing import Any

logger = logging.getLogger(__name__)
logger.setLevel(level='DEBUG')

missing_env_vars = False

def getEnvironmentVariable(name: str, dtype: type = None, default: Any = None):
    global missing_env_vars
    var = os.getenv(name)
    if var:
        if dtype:
            var = dtype(var)
        return var
    else:
        if default is None:
            logger.error(f'Environment variable {name} not found but required')
            missing_env_vars = True
        return default

def checkForMissingEnvironmentVariables():
    if missing_env_vars:
        raise RuntimeError('Missing environment variables. Check error log.')
        #logger.error('Missing environment variables.')
        #sys.exit(1)
