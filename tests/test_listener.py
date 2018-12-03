from dingdongditchcamera import listener


def test_handle_event(mocker):
    log_mock = mocker.patch('dingdongditchcamera.listener.logger')

    listener.handle_event(object(), 'test', '/path')

    log_mock.info.assert_called_with('New event: %s at %s', 'test', '/path')
