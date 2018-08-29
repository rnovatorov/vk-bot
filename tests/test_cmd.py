import pytest
from vk_bot.cmd import CmdParser, CmdParserExit


@pytest.fixture(name="cmd_parser")
def fixture_cmd_parser():
    cmd_parser = CmdParser(prog="$")

    subparsers = cmd_parser.add_subparsers()

    mul_parser = subparsers.add_parser("mul")
    mul_parser.add_argument("x", type=int)
    mul_parser.add_argument("y", type=int)
    mul_parser.set_defaults(func=lambda ns: ns.x * ns.y)

    return cmd_parser


class TestCmdParser(object):

    @pytest.mark.parametrize(["args_list", "result"], [
        [["mul", "6", "9"], 54],
        [["mul", "0", "-5"], 0],
    ])
    def test_sanity(self, cmd_parser, args_list, result):
        ns = cmd_parser.parse_args(args_list)
        assert ns.func(ns) == result

    @pytest.mark.parametrize("args_list", [
        ["-h"],
        ["--help"],
        ["mul", "-h"],
        ["mul", "--help"],
    ])
    def test_help(self, cmd_parser, args_list):
        try:
            cmd_parser.parse_args(args_list)
        except CmdParserExit as e:
            assert "usage" in e.message
        else:
            pytest.fail("Expected exception to be raised.")

    @pytest.mark.parametrize("args_list", [
        [""],
        ["foo"],
        ["mul", "42"],
        ["mul", "a", "42"],
        ["mul", "42", "b"],
        ["mul", "42", "43", "44"],
    ])
    def test_error(self, cmd_parser, args_list):
        try:
            cmd_parser.parse_args(args_list)
        except CmdParserExit as e:
            assert "usage" in e.message
            assert "error" in e.message
        else:
            pytest.fail("Expected exception to be raised.")
