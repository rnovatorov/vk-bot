from collections import defaultdict
from vk_client import VkClient
from six.moves.queue import Queue
from .workers import Producer, Consumer


class VkBot(object):

    def __init__(self, name, access_token):
        self.name = name
        self.vk = VkClient(access_token)
        self.handlers = defaultdict(list)

    def run(self):
        queue = Queue()
        blp = self.vk.BotsLongPoll.get()

        producer = Producer(queue, func=blp.get_updates)
        consumer = Consumer(queue, func=self.dispatch)

        producer.start()
        consumer.start()

    def add_handler(self, event_type, event_handler):
        self.handlers[event_type].append(event_handler)

    def on(self, event_types):

        def register(event_handler):
            for event_type in event_types:
                self.add_handler(event_type, event_handler)

            return event_handler

        return register

    def dispatch(self, event):
        for event_handler in self.handlers[event.type]:
            event_handler(event=event)
