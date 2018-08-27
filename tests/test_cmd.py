from vk_bot.cmd import CmdParser


class TestCmdParser(object):

    def test_add_subparsers(self):
        cmd_parser = CmdParser(prog="$")

        subparsers = cmd_parser.add_subparsers()

        mul_parser = subparsers.add_parser("mul")
        mul_parser.add_argument("x", type=int)
        mul_parser.add_argument("y", type=int)
        mul_parser.set_defaults(_handler=lambda ns: ns.x * ns.y)

        ns = cmd_parser.parse_args(['mul', '6', '9'])
        assert ns._handler(ns) == 6 * 9
