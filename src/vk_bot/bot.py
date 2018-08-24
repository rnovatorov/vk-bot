import threading
import collections
from six.moves import queue
import vk_client
from . import config


class VkBot(object):

    def __init__(self, name):
        self.name = name
        self.config = config.Config()
        self.vk = vk_client.VkClient(self.config.ACCESS_TOKEN)

        self.blp = self.vk.BotsLongPoll.get(self.config.GROUP_ID)
        self.q = queue.Queue()
        self.dispatcher = Dispatcher()

        self.producer = EventProducer(self.blp, self.q)
        self.consumer = EventConsumer(self.dispatcher, self.q)

    def run(self):
        self.producer.start()
        self.consumer.start()

    def event_handler(self, event_types):

        def register(func):

            for event_type in event_types:
                self.dispatcher.add_handler(event_type, func)

            return func

        return register


class Dispatcher(object):

    def __init__(self):
        self.event_handlers = collections.defaultdict(list)

    def add_handler(self, event_type, event_handler):
        self.event_handlers[event_type].append(event_handler)

    def dispatch(self, event):
        for event_handler in self.event_handlers[event.type]:
            event_handler(event)


class EventProducer(threading.Thread):

    def __init__(self, blp, q, **thread_kwargs):
        super(EventProducer, self).__init__(**thread_kwargs)
        self.blp = blp
        self.q = q

    def run(self):
        while True:
            for event in self.blp.get_updates():
                self.q.put(event)


class EventConsumer(threading.Thread):

    def __init__(self, dispatcher, q, **thread_kwargs):
        super(EventConsumer, self).__init__(**thread_kwargs)
        self.dispatcher = dispatcher
        self.q = q

    def run(self):
        while True:
            event = self.q.get()
            if event is not None:
                self.dispatcher.dispatch(event)
                self.q.task_done()
