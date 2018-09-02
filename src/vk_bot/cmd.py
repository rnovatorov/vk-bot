import shlex
import logging
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

    def add_command(self, func, name=None, args=None):
        if name is None:
            name = func.__name__

        if args is None:
            args = {}

        logging.debug("Registering %s to handle '%s', args: %s",
                      func, name, args)

        parser = self._subparsers.add_parser(
            name=name,
            description=func.__doc__
        )

        for arg, params in args.items():
            parser.add_argument(arg, **params)

        parser.set_defaults(_func=func)

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
            if not msg.text.startswith(self._prefix):
                return

            logging.debug("Got cmd: '%s'", msg.text)

            args_list = shlex.split(msg.text.lstrip(self._prefix))
            logging.debug("Args list: %s", args_list)

            try:
                ns = self._parser.parse_args(args_list)
                logging.debug("Ns: %s", ns)

            except CmdParserExit as e:
                logging.debug("CmdParserExit: %s", e)
                response = str(e) or "Unable to parse a command."

            else:
                try:
                    response = ns._func(msg, **{
                        k: v
                        for k, v in vars(ns).items()
                        if not k.startswith('_')
                    })
                except Exception as e:
                    logging.exception(e)
                    response = "Error."

            if response:
                self.vk.Message.send(msg.sender, response)
