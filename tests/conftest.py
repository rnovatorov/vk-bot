import pytest


@pytest.fixture(name="vk")
def fixture_vk(mocker):
    return mocker.patch("vk_bot.bot.VkClient")()
