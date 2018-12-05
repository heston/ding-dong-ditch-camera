import logging
import sys

from .env import Env

# The name of the Firebase app, used to construct the REST URL.
FIREBASE_APP_NAME = Env.string('DC_FIREBASE_APP_NAME', 'ding-dong-ditch')

# Path to service account credentials file
FIREBASE_KEY_PATH = Env.string('DC_FIREBASE_KEY_PATH', '/home/pi/.firebasekey')

# Firebase web API key
FIREBASE_API_KEY = Env.string('DC_FIREBASE_API_KEY')

# The path to the events collection
FIREBASE_EVENTS_PATH = 'events'

# Sets the rotation of the camera’s image. Valid values are 0, 90, 180, and 270.
CAMERA_ROTATION = Env.number('DC_CAMERA_ROTATION', 0)

# Logging
LOG_LEVEL = Env.string('DC_LOGGING_LEVEL', 'DEBUG')

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s %(name)s: %(message)s',
    level=LOG_LEVEL,
    stream=sys.stdout
)
