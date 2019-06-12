import os
import logging
from importlib import import_module

# Available environments for the project
_availableEnvironments = [
    'development',
    'production',
    'test'
]

# Retrieve current environment and check if it is valid
env = os.getenv('ENVIRONMENT', 'development')

if env not in _availableEnvironments:
    logging.warning('Environment specified is not available. Falling back to "development" environment.')
    env = 'development'

# Try to import the configurations of that environment
try:
    config = import_module('main.config.' + env).config
except Exception, e:
    logging.exception('Could not find config for the environment: ' + env, e)
    raise e
