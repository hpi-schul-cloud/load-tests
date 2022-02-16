
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level='DEBUG')

missing_env_vars = False

def getEnvironmentVariable(name: str, dtype: type = None, required: bool = True):
    var = os.getenv(name)
    logger.error(f'os.getenv({name}) -> {var=}')
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
