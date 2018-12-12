from datetime import timedelta
import logging

from firebasedata import LiveData
import pyrebase

from . import camera
from . import settings

logger = logging.getLogger(__name__)

NAME = 'firebase'
DATABASE_URL = 'https://{}.firebaseio.com'.format(settings.FIREBASE_APP_NAME)
AUTH_DOMAIN = '{}.firebaseapp.com'.format(settings.FIREBASE_APP_NAME)
STORAGE_BUCKET = '{}.appspot.com'.format(settings.FIREBASE_APP_NAME)
TTL = timedelta(minutes=75)

VALID_EVENTS = (
    'doorbell',
)

firebase_config = {
    'apiKey': settings.FIREBASE_API_KEY,
    'authDomain': AUTH_DOMAIN,
    'databaseURL': DATABASE_URL,
    'storageBucket': STORAGE_BUCKET,
    'serviceAccount': settings.FIREBASE_KEY_PATH,
}
firebase_app = pyrebase.initialize_app(firebase_config)
live_data = LiveData(firebase_app, settings.FIREBASE_EVENTS_PATH, TTL)
storage = firebase_app.storage()


def get_image_path(event_path):
    if not event_path:
        raise ValueError('No event path specified')

    parts = event_path.split('/')
    key = parts[-1]
    unit = parts[-2]
    return '{}/{}/{}.jpg'.format(settings.FIREBASE_EVENTS_PATH, unit, key)


def store_image(event_path, stream):
    logger.debug('Storing image %s for event %s', event_path, stream)
    path = get_image_path(event_path)
    storage.child(path).put(stream)
    return path


def handle_event(sender, value=None, path=None):
    logger.info('New event: %s at %s', value, path)

    # If this event is empty, or at the root path, ignore it
    if value is None or path == '/':
        return None

    # If the child value is invalid, ignore it
    try:
        child_value = value.get(path)
        if child_value is None or child_value.get('name') not in VALID_EVENTS:
            return None
    except AttributeError:
        return None

    try:
        image = camera.capture_to_stream()
        return store_image(path, image)
    except Exception as e:
        logger.error('Unable to save image: %s', e, exc_info=True)


live_data.signal('/').connect(handle_event)


def listen():
    live_data.get_data()
