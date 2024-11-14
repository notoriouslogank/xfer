import argparse
import sys
from pathlib import Path
from time import sleep

from prompt_toolkit import PromptSession

from src.client import Client
from src.packer import Compressor
from src.server import RemoteHost

parser = argparse.ArgumentParser(
    prog="xfer",
    description="Application to send/receive files to/from remote machine.",
    epilog="Thanks for playing",
)

parser.add_argument(
    "-s",
    "--send",
    nargs="?",
    help="Send file(s) to IP.",
    required=False,
    default=argparse.SUPPRESS,
)

parser.add_argument(
    "-p",
    "--port",
    help="Remote host port",
    nargs="?",
    type=int,
    required=False,
    default=argparse.SUPPRESS,
)

parser.add_argument(
    "-f",
    "--file",
    help="Absolute or relative path to file or directory to send",
    nargs="?",
    type=Path,
    required=False,
    default=argparse.SUPPRESS,
)

parser.add_argument(
    "-r",
    "--receive",
    required=False,
    help="Listen for incoming connections.",
    action="store_true",
    default=argparse.SUPPRESS,
)


args = parser.parse_args()


def prepare_cli():

    try:
        if args.send:
            if args.send == None:
                raise Exception("Missing value for args.send")
            elif args.send != None:
                host_ip = args.send
        else:
            raise Exception("Missing args.send")
    except Exception:
        host_ip = "192.168.0.13"

    try:
        if args.port:
            if args.port == None:
                raise Exception("Missing value for args.port")
            elif args.port != None:
                host_port = args.port
        else:
            raise Exception("Missing args.port")
    except Exception:
        host_port = 5002

    try:
        if args.file:
            if args.file == None:
                raise Exception("Missing value for args.file")
            elif args.file != None:
                filename = args.file
        else:
            raise Exception("Missing args.file")
    except Exception:
        filename = "."
    return host_ip, host_port, filename


def cli_receive():
    server = RemoteHost()
    filename = server.receive()
    print(filename)
    return filename


def cli_send(host, port, filename):
    client = Client()
    client.send(host, port, filename)
    sys.exit()


def main():
    flow = 0
    session = PromptSession()
    while flow == 0:
        try:
            choice = session.prompt("Send or Receive?\n[S/r]\n>> ")
            flow += 1
        except KeyboardInterrupt:
            sys.exit()
        else:
            if str(choice).lower() == "s":
                client = Client()
                host, port = client.get_server_info()
                client.send(host, port)
            elif str(choice).lower() == "r":
                server = RemoteHost()
                while True:
                    try:
                        server.receive()
                    except KeyboardInterrupt:
                        sys.exit()
            if str(choice).lower() == "q":
                print(f"Closing application\n")
                sleep(0.1)
                sys.exit()


if len(sys.argv) > 1:
    try:
        if args.receive == True:
            print("Waiting for file(s)...")
            Compressor.unpack(cli_receive())
    except Exception:
        pass
        host, port, file = prepare_cli()
        cli_send(host, port, file)

if __name__ == "__main__":
    main()
