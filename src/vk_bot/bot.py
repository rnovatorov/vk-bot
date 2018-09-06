import logging
from collections import defaultdict
from vk_client import VkClient
from .concur import Queue, Producer, Consumer


class VkBot(object):

    def __init__(self, access_token):
        self.vk = VkClient(access_token)

        self._queue = Queue()
        self._workers = []
        self._event_handlers = defaultdict(list)

    def add_event_handler(self, event_type, event_handler):
        logging.debug('Registering %s to handle %s',
                      event_handler, event_type)
        self._event_handlers[event_type].append(event_handler)

    def on(self, event_types):
        """
        Decorator version of `self.add_event_handler`.
        """
        def registering_wrapper(event_handler):
            for event_type in event_types:
                self.add_event_handler(event_type, event_handler)
            return event_handler

        return registering_wrapper

    def run(self, n_workers):
        logging.debug('Running with %d workers', n_workers)
        blp = self.vk.BotsLongPoll.get()

        self._workers.append(Producer(
            queue=self._queue,
            func=blp.get_updates,
            name='Producer'
        ))

        for i in range(n_workers):
            self._workers.append(Consumer(
                queue=self._queue,
                func=self._dispatch_event,
                name='Consumer-%d' % i
            ))

        for worker in self._workers:
            logging.debug('Starting %s', worker.name)
            worker.start()

    def _dispatch_event(self, event):
        for event_handler in self._event_handlers[event.type]:
            logging.debug('Dispatching %s to %s', event, event_handler)
            event_handler(event.object)
