import pytest
import vk_bot
from vk_client.enums import GroupEventType


@pytest.fixture(name="bot")
def fixture_bot():
    return vk_bot.VkBot(access_token=None)


def test_event_dispatching(mocker, bot):
    event_mock = mocker.Mock()
    event_handler_stub = mocker.stub()

    bot.add_event_handler(event_mock.type, event_handler_stub)
    bot._dispatch_event(event_mock)

    event_handler_stub.assert_called_once_with(event_mock.object)
