#!/usr/bin/env python3.10
"""
Server that accepts every requests, accepts any input, but does nothing.
"""
import threading
from socket import *

import click
import paramiko
from paramiko import Transport, Channel


class EchoSubsystem(paramiko.SubsystemHandler):
    def start_subsystem(
        self, name: str, transport: Transport, channel: Channel
    ) -> None:
        host, port = transport.getpeername()
        print(
            f"Subsystem started: {name!r} on {host}:{port} (channel ID {channel.chanid})"
        )

        while True:
            incoming = channel.recv(1024)
            print(f"Handling incoming data: {incoming!r}")

            channel.send(incoming)

    def finish_subsystem(self) -> None:
        print(f"Subsystem finished")


class SubsystemInterface(paramiko.ServerInterface):
    def get_allowed_auths(self, username: str) -> str:
        return "none"

    def check_auth_none(self, username: str) -> int:
        print(f"user {username} authenticated")
        return paramiko.common.AUTH_SUCCESSFUL

    def check_channel_request(self, kind: str, chanid: int) -> int:
        print(f"channel request {kind!r} on {chanid} accepted")
        return paramiko.common.OPEN_SUCCEEDED

    @classmethod
    def run(cls, client: socket, addr: str, key: paramiko.RSAKey) -> threading.Thread:
        def _thread_main():
            server = cls()

            transport = paramiko.Transport(client)
            transport.add_server_key(key)
            transport.set_subsystem_handler("echo", EchoSubsystem)
            transport.start_server(server=server)

            transport.join()

            print(f"{addr} terminated connection")

        res = threading.Thread(target=_thread_main)
        res.daemon = True
        res.start()

        return res


@click.command(help="Echo subsystem server")
@click.option(
    "-h", "--host", default="localhost", show_default=True, help="SSH server host"
)
@click.option(
    "-p", "--port", type=int, default=10022, show_default=True, help="SSH server port"
)
def main(host, port):
    key = paramiko.RSAKey.generate(2048)

    sock = socket(AF_INET, SOCK_STREAM, IPPROTO_IP)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)

    while True:
        client, addr = sock.accept()
        addr = f"{addr[0]}:{addr[1]}"
        print(f"Incoming connection from {addr}")

        SubsystemInterface.run(client, addr, key)


if __name__ == "__main__":
    exit(main())
