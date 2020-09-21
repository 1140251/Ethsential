import sys
from .src.applications.server import ETHSENTIAL
from .src.applications.cli import CLI
from .src.parser import create_parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.action == 'cli':
        try:
            CLI.exec_cmd(args)
        except Exception as e:
            if hasattr(e, 'message'):
                print(getattr(e, 'message', repr(e)))
            else:
                print(e)
            sys.exit(0)
    elif args.action == 'install':
        try:
            CLI.install()
        except Exception as e:
            if hasattr(e, 'message'):
                print(getattr(e, 'message', repr(e)))
            else:
                print(e)
    elif args.action == 'tcp':
        ETHSENTIAL.start_tcp(args.host, args.port)
    else:
        ETHSENTIAL.start_io()


if __name__ == '__main__':
    main()
