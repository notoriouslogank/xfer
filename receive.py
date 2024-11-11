import os
import socket
import subprocess

import tqdm
from rich import print as pprint

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"


def receive():
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    pprint(f"[+] Listening as {SERVER_HOST}:{SERVER_PORT}")
    client_socket, address = s.accept()
    pprint(f"[+] {address} is connected")

    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)

    progress = tqdm.tqdm(
        range(filesize),
        f"Receiving {filename}",
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    )
    with open(filename, "wb") as f:
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))

    client_socket.close()
    s.close()


def unpack():
    subprocess.call(["tar", "-xf", "*.tar.gz"])


def main():
    receive()
    unpack()
