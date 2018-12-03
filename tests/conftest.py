import pytest


@pytest.fixture(autouse=True)
def camera_timer(mocker):
    return mocker.patch('dingdongditchcamera.camera.time')
