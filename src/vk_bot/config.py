import os


class Config(object):

    ENV_VAR_PREFIX = 'VK_BOT'
    ACCESS_TOKEN = os.getenv('_'.join([ENV_VAR_PREFIX, 'ACCESS_TOKEN']))
