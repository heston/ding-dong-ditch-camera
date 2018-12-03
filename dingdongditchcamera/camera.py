import atexit
import io
import time

import picamera

_camera = None


def get_camera():
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
    camera.capture(stream, 'jpeg')
    stream.seek(0)
    return stream


@atexit.register
def close_camera():
    global _camera
    camera = get_camera()
    camera.stop_preview()
    camera.close()
    _camera = None
