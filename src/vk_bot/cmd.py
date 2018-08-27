from argparse import ArgumentParser


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

        msg = self._msg_buff or "No message."
        self._msg_buff = ""

        raise CmdParserExit(msg)
