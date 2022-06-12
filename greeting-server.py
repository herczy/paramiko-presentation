#!/usr/bin/env python3
"""
Simple greeting server.
"""

from socket import *

import click
import paramiko


class GreetServerInterface(paramiko.ServerInterface):
    def check_channel_request(self, kind: str, chanid: int) -> int:
        if kind == "session" and chanid == 0:
            print(f"OPEN_SUCCEEDED: Allowing {kind!r}, channel ID {chanid}")
            return paramiko.common.OPEN_SUCCEEDED

        print(
            f"OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED: Not allowing {kind!r}, channel ID {chanid}"
        )
        return paramiko.common.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username: str, password: str) -> int:
        if username == password:
            print(
                f"AUTH_SUCCESSFUL: Authenticating {username!r} with password {password!r}"
            )
            return paramiko.common.AUTH_SUCCESSFUL

        print(f"AUTH_FAILED: Authenticating {username!r} with password {password!r}")
        return paramiko.common.AUTH_FAILED

    def check_channel_shell_request(self, channel: paramiko.Channel) -> bool:
        print(f"Shell request on channel {channel.chanid}")
        return True


@click.command(help="Echo server")
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
        print(f"Incoming connection from {addr}")

        server = GreetServerInterface()

        transport = paramiko.Transport(client)
        transport.add_server_key(key)
        transport.start_server(server=server)

        channel = transport.accept()
        username = transport.get_username()

        channel.send(f"Greetings, {username}!\r\n".encode())
        channel.send_exit_status(0)
        channel.close()


if __name__ == "__main__":
    exit(main())
