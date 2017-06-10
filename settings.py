"""
Flask Api Settings
Mike Tung
"""

import os

# Check environment to apply environment specific settings
ENV = os.environ.get('APP_ENV', 'DEV')

# Common settings here
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 3000))
API_USER = os.environ.get('API_USER', None)
API_PW = os.environ.get('API_PW', None)

# Mongo settings
MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.environ.get('MONGO_PORT', 27017))
MONGO_DB = os.environ.get('MONGO_DB', None)

# For each environment setting, some common settings maybe overridden
if ENV is 'PROD':
    DEBUG = False
    MULTITHREADING = True

else:
    DEBUG = True
    MULTITHREADING = False
