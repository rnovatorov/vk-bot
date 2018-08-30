from collections import defaultdict
from vk_client import VkClient
from six.moves.queue import Queue
from .cmd import CmdHandlerMixin
from .workers import Producer, Consumer


class VkBot(CmdHandlerMixin):

    def __init__(self, access_token, n_workers=1):
        super(VkBot, self).__init__()

        self.vk = VkClient(access_token)

        self._queue = Queue()
        self._workers = []
        self._n_workers = n_workers
        self._event_handlers = defaultdict(list)

        self._enable_cmd_handler()

    def add_event_handler(self, event_type, event_handler):
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

    def run(self):
        blp = self.vk.BotsLongPoll.get()

        self._workers.append(Producer(
            queue=self._queue,
            func=blp.get_updates
        ))

        for _ in range(self._n_workers):
            self._workers.append(Consumer(
                queue=self._queue,
                func=self._dispatch_event
            ))

        for worker in self._workers:
            worker.start()

    def _dispatch_event(self, event):
        for event_handler in self._event_handlers[event.type]:
            event_handler(event.object)
