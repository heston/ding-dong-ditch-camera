import logging
import os
import sys

# The name of the Firebase app, used to construct the REST URL.
FIREBASE_APP_NAME = os.getenv('DC_FIREBASE_APP_NAME', 'ding-dong-ditch')

# Path to service account credentials file
FIREBASE_KEY_PATH = os.getenv('DC_FIREBASE_KEY_PATH', '/home/pi/.firebasekey')

# Firebase web API key
FIREBASE_API_KEY = os.getenv('DC_FIREBASE_API_KEY')

# The path to the events collection
FIREBASE_EVENTS_PATH = 'events'

# Logging
LOG_LEVEL = os.getenv('DC_LOGGING_LEVEL', 'DEBUG')

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s %(name)s: %(message)s',
    level=LOG_LEVEL,
    stream=sys.stdout
)
