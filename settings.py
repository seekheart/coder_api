"""
Flask Api Settings
Mike Tung
"""

import os

# Check environment to apply environment specific settings
ENV = os.environ.get('APP_ENV', 'DEV')

# Common settings here
PORT = int(os.environ.get('PORT', 3000))

# Mongo settings
MONGO_COLLECTIONS = {
    'programming_language': 'languages',
    'users': 'users'}
MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.environ.get('MONGO_PORT', 27017))
MONGO_DB = os.environ.get('MONGO_DB', None)

# For each environment setting, some common settings maybe overridden
if ENV is 'PROD':
    HOST = os.environ.get('HOST', None)
    int(PORT=os.environ.get('PORT', None))
    DEBUG = False
    MULTITHREADING = True
else:
    HOST = '0.0.0.0'
    DEBUG = True
    MULTITHREADING = False
