from vk_bot.ext.testing import Scenario
from vk_bot.dispatcher import Dispatcher


def test_event_dispatching(mocker):
    event_mock = mocker.Mock()
    event_handler_stub = mocker.stub()

    scenario = Scenario([
        lambda: [event_mock]
    ])

    dispatcher = Dispatcher(scenario)
    dispatcher.add_event_handler(event_mock.type, event_handler_stub)

    dispatcher.run()
    scenario.finished.wait()
    dispatcher.stop()

    event_handler_stub.assert_called_once_with(event_mock.object)
