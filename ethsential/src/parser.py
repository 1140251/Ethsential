import argparse
from .tools.tool_factory import ToolFactory


def add_arguments(parser):
    sub = parser.add_subparsers(dest='action')
    tcp = sub.add_parser('tcp', help="Use TCP server")
    cli = sub.add_parser('cli', help="Use command line interface")
    sub.add_parser(
        'install', aliases=['i', 'isntall', 'add'], help="Install tools")

    tcp.add_argument('--host',
                     default="127.0.0.1",
                     help="Bind to address"
                     )
    tcp.add_argument('-p', '--port',
                     type=int,
                     default=2087,
                     help="Bind to port"
                     )

    cli.add_argument('-f', '--file',
                     nargs='+',
                     default=[],
                     help='select file(s) or directories to be analysed', required=True)
    cli.add_argument('-t', '--tools',
                     choices=ToolFactory.TOOLS_CHOICES,
                     nargs='+',
                     help='select tool(s)', required=True)
    cli.add_argument('-op', '--outputPath',
                     type=str,
                     default="result/",
                     help='The full path for the new output directory, relative to the current workspace. By default, writes output to a folder named result/ in the current workspace.')


def create_parser():
    parser = argparse.ArgumentParser(
        description='Security analysis for Ethereum smart contracts')
    add_arguments(parser)
    return parser
