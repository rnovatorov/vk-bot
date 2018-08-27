import shlex
from collections import defaultdict
from vk_client import VkClient
from vk_client.enums import GroupEventType
from six.moves.queue import Queue
from .workers import Producer, Consumer
from .cmd import CmdParser, CmdParserExit


class VkBot(object):

    def __init__(
        self,
        access_token,
        cmd_prefix="$",
        enable_cmd_handler=True
    ):
        self.vk = VkClient(access_token)

        self._event_handlers = defaultdict(list)

        self.cmd_prefix = cmd_prefix
        self._cmd_parser = CmdParser(prog=cmd_prefix)
        self._cmd_subparsers = self._cmd_parser.add_subparsers(
            parser_class=CmdParser
        )

        if enable_cmd_handler:
            self._enable_cmd_handler()

    def run(self):
        queue = Queue()
        blp = self.vk.BotsLongPoll.get()

        producer = Producer(queue, func=blp.get_updates)
        consumer = Consumer(queue, func=self._dispatch_event)

        producer.start()
        consumer.start()

    def _add_event_handler(self, event_type, event_handler):
        self._event_handlers[event_type].append(event_handler)

    def on(self, event_types):

        def registering_wrapper(event_handler):
            for event_type in event_types:
                self._add_event_handler(event_type, event_handler)

            return event_handler

        return registering_wrapper

    def _enable_cmd_handler(self):

        @self.on([GroupEventType.MESSAGE_NEW])
        def handle_cmd(msg):

            if msg.text.startswith(self.cmd_prefix):
                args_list = shlex.split(msg.text.lstrip(self.cmd_prefix))

                try:
                    ns = self._cmd_parser.parse_args(args_list)
                except CmdParserExit as e:
                    self.vk.Message.send(
                        peer=msg.sender,
                        message=str(e)
                    )
                else:
                    ns._handler(msg, ns)

    def _add_command(self, name, cmd, args_defs):
        parser = self._cmd_subparsers.add_parser(name)

        for name_or_flags, params in args_defs:
            parser.add_argument(*name_or_flags, **params)

        parser.set_defaults(_handler=cmd)

    def command(self, name, args_defs):

        def registering_wrapper(cmd):
            self._add_command(name, cmd, args_defs)
            return cmd

        return registering_wrapper

    def _dispatch_event(self, event):
        for event_handler in self._event_handlers[event.type]:
            event_handler(event.object)
