
import unittest
from io import StringIO
from unittest.mock import patch
from .parser import create_parser


class ParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = create_parser()

    def test_pass(self):
        _ = self.parser.parse_args([])

    def test_tcp_pass(self):
        parsed = self.parser.parse_args(['tcp'])
        self.assertEqual(parsed.action, 'tcp')

    @patch('sys.stderr', new_callable=StringIO)
    def test_cli_fail(self, mock_stderr):
        with self.assertRaises(SystemExit):
            _ = self.parser.parse_args(['cli'])
        self.assertRegex(mock_stderr.getvalue(
        ), 'the following arguments are required: -f/--file, -t/--tool')

    def test_cli_full_pass(self):
        parsed = self.parser.parse_args(
            ['cli', '-f', 'test', 'p', '-t', 'all', 'mythril', '-op', 'example'])
        self.assertEqual(parsed.action, 'cli')

    @patch('sys.stderr', new_callable=StringIO)
    def test_cli_fail_tool(self, mock_stderr):
        with self.assertRaises(SystemExit):
            _ = self.parser.parse_args(['cli', '-f', 'test', '-t', 'tool'])
        self.assertRegex(mock_stderr.getvalue(), r"invalid choice: 'tool'")

    @patch('sys.stderr', new_callable=StringIO)
    def test_cli_empty_file(self, mock_stderr):
        with self.assertRaises(SystemExit):
            _ = self.parser.parse_args(['cli', '-f', '-t', 'all'])
        self.assertRegex(mock_stderr.getvalue(),
                         'argument -f/--file: expected at least one argument')

    @patch('sys.stderr', new_callable=StringIO)
    def test_cli_empty_tool(self, mock_stderr):
        with self.assertRaises(SystemExit):
            _ = self.parser.parse_args(['cli', '-f', 'file', '-t'])
        self.assertRegex(mock_stderr.getvalue(),
                         'argument -t/--tools: expected at least one argument')
