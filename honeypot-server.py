#!/usr/bin/env python3.10
"""
Server that accepts every requests, accepts any input, but does nothing.
"""
import threading
from select import select
from socket import *

import click
import paramiko


class HoneypotInterface(paramiko.ServerInterface):
    def get_allowed_auths(self, username: str) -> str:
        return "password"

    def check_auth_password(self, username: str, password: str) -> int:
        print(f"Authenticating {username!r} with password {password!r}")
        return paramiko.common.AUTH_SUCCESSFUL

    def check_port_forward_request(self, address: str, port: int) -> int:
        print(f"Attempted to port forward {address}:{port}")
        return False

    def check_global_request(self, kind: str, msg: paramiko.Message):
        return False

    def check_channel_pty_request(
        self,
        channel: paramiko.Channel,
        term: str,
        width: int,
        height: int,
        pixelwidth: int,
        pixelheight: int,
        modes: str,
    ) -> bool:
        print(f"PTY request for channel {channel.chanid}: {term} {width}x{height}")
        return True

    def check_channel_exec_request(
        self, channel: paramiko.Channel, command: bytes
    ) -> bool:
        print(f"Attempting to execute command on channel {channel.chanid}: {command!r}")
        return True

    def check_channel_window_change_request(
        self,
        channel: paramiko.Channel,
        width: int,
        height: int,
        pixelwidth: int,
        pixelheight: int,
    ) -> bool:
        print(f"Window change request for channel {channel.chanid}: {width}x{height}")
        return True

    def check_channel_request(self, kind: str, chanid: int) -> int:
        print(f"OPEN_SUCCEEDED: Allowing {kind!r}, channel ID {chanid}")
        return paramiko.common.OPEN_SUCCEEDED

    def check_channel_shell_request(self, channel: paramiko.Channel) -> bool:
        print(f"Shell request on channel {channel.chanid}")
        return True

    @classmethod
    def run(cls, client: socket, addr: str, key: paramiko.RSAKey) -> threading.Thread:
        def _thread_main():
            server = cls()

            transport = paramiko.Transport(client)
            transport.add_server_key(key)
            transport.start_server(server=server)

            channel = transport.accept()

            while transport.is_active():
                select([client], [], [], 1.0)
                if channel.recv_ready():
                    incoming = channel.recv(1024)
                    print(f"Received {len(incoming)} byte(s) on channel")

            channel.close()
            transport.close()

            print(f"{addr} terminated connection")

        res = threading.Thread(target=_thread_main)
        res.daemon = True
        res.start()

        return res


@click.command(help="Honeypot server")
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

        HoneypotInterface.run(client, addr, key)


if __name__ == "__main__":
    exit(main())
