import shlex
from argparse import ArgumentParser
from vk_client.enums import GroupEventType


class CmdParserExit(Exception):
    pass


class CmdParser(ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(CmdParser, self).__init__(*args, **kwargs)
        self._msg_buff = ""

    def _print_message(self, message, file=None):
        self._msg_buff += message

    def exit(self, status=0, message=None):
        if message:
            self._print_message(message)

        msg, self._msg_buff = self._msg_buff, ""

        raise CmdParserExit(msg)


class CmdHandlerMixin(object):

    vk = NotImplemented
    on = NotImplemented

    def __init__(self, prefix="$ "):
        self._prefix = prefix
        self._parser = CmdParser(prog=prefix)
        self._subparsers = self._parser.add_subparsers(
            parser_class=CmdParser
        )

    def add_command(self, func, name, args_defs):
        parser = self._subparsers.add_parser(name)

        for name_or_flags, params in args_defs:
            parser.add_argument(*name_or_flags, **params)

        parser.set_defaults(func=func)

    def command(self, *args, **kwargs):
        """
        Decorator version of `self.add_command`.
        """
        def registering_wrapper(func):
            self.add_command(func, *args, **kwargs)
            return func

        return registering_wrapper

    def _enable_cmd_handler(self):

        @self.on([GroupEventType.MESSAGE_NEW])
        def handle_cmd(msg):

            if msg.text.startswith(self._prefix):
                args_list = self._parse_cmd(msg.text)

                try:
                    ns = self._parser.parse_args(args_list)
                except CmdParserExit as e:
                    self.vk.Message.send(
                        peer=msg.sender,
                        message=str(e) or "Unable to parse a command."
                    )
                else:
                    ns.func(msg, ns)

    def _parse_cmd(self, string):
        return shlex.split(string.lstrip(self._prefix))
