from .src.applications.server import ETHSENTIAL
from .src.applications.cli import CLI
from .src.parser import create_parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.action == 'cli':
        CLI.exec_cmd(args)
    elif args.action == 'install':
        CLI.install()
    elif args.action == 'tcp':
        ETHSENTIAL.start_tcp(args.host, args.port)
    else:
        ETHSENTIAL.start_io()


if __name__ == '__main__':
    main()
