import io
import picamera

from dingdongditchcamera import camera


def teardown_function(function):
    camera._camera = None


def test_get_camera__initial():
    result = camera.get_camera()

    assert result == picamera.PiCamera.return_value


def test_get_camera__repeat():
    result1 = camera.get_camera()
    result2 = camera.get_camera()

    assert result1 is result2


def test_get_camera__creates_camera():
    camera.get_camera()

    assert picamera.PiCamera.called


def test_get_camera__starts_preview():
    camera.get_camera()

    assert picamera.PiCamera.return_value.start_preview.called


def test_get_camera__waits_for_camera(camera_timer):
    camera.get_camera()

    camera_timer.sleep.assert_called_with(2)


def test_capture_to_stream__returns_stream():
    result = camera.capture_to_stream()

    assert isinstance(result, io.BytesIO)


def test_capture_to_stream__calls_capture():
    result = camera.capture_to_stream()

    camera._camera.capture.assert_called_with(result, 'jpeg')


def test_capture_to_stream__rewinds_stream(mocker):
    mocker.patch('dingdongditchcamera.camera.io')
    result = camera.capture_to_stream()

    result.seek.assert_called_with(0)


def test_close_camera__calls_stop_preview():
    stale_camera = camera.get_camera()
    camera.close_camera()

    assert stale_camera.stop_preview.called


def test_close_camera__calls_close():
    stale_camera = camera.get_camera()
    camera.close_camera()

    assert stale_camera.close.called


def test_close_camera__unlinks_camera():
    camera.close_camera()

    assert camera._camera is None
