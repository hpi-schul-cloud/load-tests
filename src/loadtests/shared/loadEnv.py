
import os
import logging

logger = logging.getLogger(__name__)

missing_env_vars = False

def getEnvironmentVariable(name: str, dtype: type = None, required: bool = True):
    var = os.environ.get(name)
    if var:
        if dtype:
            var = dtype(var)
        return var
    else:
        if required:
            logger.error(f'Environment variable {name} not found but required')
            missing_env_vars = True
        return None

def checkForMissingEnvironmentVariables():
    if missing_env_vars:
        raise RuntimeError('Missing environment variables. Check error log.')
