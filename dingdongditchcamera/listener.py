from datetime import timedelta
import logging

from firebasedata import LiveData
import pyrebase

from . import main
from . import settings

logger = logging.getLogger(__name__)

NAME = 'firebase'
DATABASE_URL = 'https://{}.firebaseio.com'.format(settings.FIREBASE_APP_NAME)
AUTH_DOMAIN = '{}.firebaseapp.com'.format(settings.FIREBASE_APP_NAME)
STORAGE_BUCKET = '{}.appspot.com'.format(settings.FIREBASE_APP_NAME)
TTL = timedelta(minutes=75)

firebase_config = {
    'apiKey': settings.FIREBASE_API_KEY,
    'authDomain': AUTH_DOMAIN,
    'databaseURL': DATABASE_URL,
    'storageBucket': STORAGE_BUCKET,
    'serviceAccount': settings.FIREBASE_KEY_PATH,
}
firebase_app = pyrebase.initialize_app(firebase_config)
live_data = LiveData(firebase_app, settings.FIREBASE_EVENTS_PATH, TTL)


def handle_event(sender, value=None):
    logger.info('New event: %s', value)


live_data.signal('/').connect(handle_event)


def listen():
    live_data.get_data()
