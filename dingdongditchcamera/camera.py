import atexit
import io
import logging
import time

import picamera

logger = logging.getLogger(__name__)
_camera = None


def get_camera():
    logger.info('Warming up camera...')
    global _camera
    if _camera:
        return _camera

    _camera = picamera.PiCamera()
    _camera.start_preview()
    time.sleep(2)  # Camera warm-up time
    return _camera


def capture_to_stream():
    camera = get_camera()
    stream = io.BytesIO()
    logger.debug('Capturing image to stream: %s', stream)
    camera.capture(stream, 'jpeg')
    stream.seek(0)
    return stream


@atexit.register
def close_camera():
    logger.info('Shutting down camera...')
    global _camera
    camera = get_camera()
    camera.stop_preview()
    camera.close()
    _camera = None
