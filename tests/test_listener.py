import pytest

from firebasedata import FirebaseData

from dingdongditchcamera import listener


def test_get_image_path__no_path():
    with pytest.raises(ValueError):
        listener.get_image_path(None)


def test_get_image_path__bad_path():
    with pytest.raises(IndexError):
        listener.get_image_path('asdf')


def test_get_image_path__good_path():
    event_path = '/events/1234/a-s-d-f'
    image_path = listener.get_image_path(event_path)

    assert image_path == 'events/1234/a-s-d-f.jpg'


def test_store_image(mocker):
    event_path = '/events/1234/a-s-d-f'
    image_path = 'events/1234/a-s-d-f.jpg'
    mocker.patch('dingdongditchcamera.listener.get_image_path').return_value = image_path
    image_stream = object()

    listener.store_image(event_path, image_stream)

    listener.storage.child.assert_called_with(image_path)
    listener.storage.child.return_value.put.assert_called_with(image_stream)


def test_handle_event__logging(mocker):
    log_mock = mocker.patch('dingdongditchcamera.listener.logger')
    data = FirebaseData()

    listener.handle_event(object(), data, '/path')

    log_mock.info.assert_called_with('New event: %s at %s', data, '/path')


def test_handle_event__missing_value(mocker):
    camera_mock = mocker.patch('dingdongditchcamera.listener.camera')

    listener.handle_event(object(), None, '/path')

    assert not camera_mock.capture_to_stream.called


def test_handle_event__invalid_value(mocker):
    camera_mock = mocker.patch('dingdongditchcamera.listener.camera')

    listener.handle_event(object(), 'test', '/path')

    assert not camera_mock.capture_to_stream.called


def test_handle_event__root_path(mocker):
    camera_mock = mocker.patch('dingdongditchcamera.listener.camera')
    data = FirebaseData()

    listener.handle_event(object(), data, '/')

    assert not camera_mock.capture_to_stream.called


def test_handle_event__empty_child(mocker):
    camera_mock = mocker.patch('dingdongditchcamera.listener.camera')
    data = FirebaseData()

    listener.handle_event(object(), data, '/foo/bar')

    assert not camera_mock.capture_to_stream.called


def test_handle_event__invalid_child(mocker):
    camera_mock = mocker.patch('dingdongditchcamera.listener.camera')
    data = FirebaseData()
    data.set('/foo/bar', {'name': 'huh'})

    listener.handle_event(object(), data, '/foo/bar')

    assert not camera_mock.capture_to_stream.called


def test_handle_event__capture_raises(mocker):
    log_mock = mocker.patch('dingdongditchcamera.listener.logger')
    camera_mock = mocker.patch('dingdongditchcamera.listener.camera')
    error = RuntimeError('boom')
    camera_mock.capture_to_stream.side_effect = error
    data = FirebaseData()
    data.set('/foo', {'name': 'doorbell'})

    listener.handle_event(object(), data, '/foo')

    log_mock.error.assert_called_with('Unable to save image: %s', error, exc_info=True)


def test_handle_event__store_image_raises(mocker):
    log_mock = mocker.patch('dingdongditchcamera.listener.logger')
    store_image_mock = mocker.patch('dingdongditchcamera.listener.store_image')
    error = RuntimeError('boom')
    store_image_mock.side_effect = error
    data = FirebaseData()
    data.set('/foo', {'name': 'doorbell'})

    listener.handle_event(object(), data, '/foo')

    log_mock.error.assert_called_with('Unable to save image: %s', error, exc_info=True)


def test_handle_event__success(mocker):
    log_mock = mocker.patch('dingdongditchcamera.listener.logger')
    camera_mock = mocker.patch('dingdongditchcamera.listener.camera')
    store_image_mock = mocker.patch('dingdongditchcamera.listener.store_image')
    data = FirebaseData()
    data.set('/foo', {'name': 'doorbell'})

    result = listener.handle_event(object(), data, '/foo')

    assert camera_mock.capture_to_stream.called
    store_image_mock.assert_called_with(
        '/foo',
        camera_mock.capture_to_stream.return_value
    )
    assert result == store_image_mock.return_value
    assert not log_mock.error.called


def test_listen():
    listener.listen()
    assert True
