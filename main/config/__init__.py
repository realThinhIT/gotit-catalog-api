import os
import importlib

# Retrieve current environment, if one is not specified, fallback to 'development'
env = os.getenv('ENVIRONMENT', 'development')

# Try to import the configurations of that environment
try:
    config = importlib.import_module('main.config.' + env).config
except ImportError, e:
    raise Exception('Could not find config for the environment: "{}". '
                    'Please correct environment name and try again.'.format(env))
