import threading
import collections
import vk_client
from six.moves import queue
from . import config


class VkBot(object):

    def __init__(self, name):
        self.name = name
        self.config = config.Config()
        self.vk = vk_client.VkClient(self.config.ACCESS_TOKEN)
        self.dispatcher = Dispatcher()

    def run(self):
        q = queue.Queue()
        blp = self.vk.BotsLongPoll.get()

        producer = EventProducer(q, blp, ame="EventsProducer")
        consumer = EventConsumer(q, self.dispatcher, name="EventsConsumer")

        producer.start()
        consumer.start()

    def on(self, event_types):

        def register(event_handler):
            for event_type in event_types:
                self.dispatcher.add_handler(event_type, event_handler)

            return event_handler

        return register


class Dispatcher(object):

    def __init__(self):
        self.handlers = collections.defaultdict(list)

    def add_handler(self, event_type, event_handler):
        self.handlers[event_type].append(event_handler)

    def dispatch(self, event):
        for event_handler in self.handlers[event.type]:
            event_handler(event)


class EventProducer(threading.Thread):

    def __init__(self, q, blp, **thread_kwargs):
        super(EventProducer, self).__init__(**thread_kwargs)
        self.q = q
        self.blp = blp

    def run(self):
        while True:
            for event in self.blp.get_updates():
                self.q.put(event)


class EventConsumer(threading.Thread):

    def __init__(self, q, dispatcher, **thread_kwargs):
        super(EventConsumer, self).__init__(**thread_kwargs)
        self.q = q
        self.dispatcher = dispatcher

    def run(self):
        while True:
            event = self.q.get()
            if event is not None:
                self.dispatcher.dispatch(event)
                self.q.task_done()
