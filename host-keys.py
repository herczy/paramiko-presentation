#!/usr/bin/env python3.10

"""
Execute a single command on the given SSH server
"""
import base64
import os.path

import click
import paramiko


class AskPolicy(paramiko.MissingHostKeyPolicy):
    def missing_host_key(
        self, client: paramiko.SSHClient, hostname: str, key: paramiko.PKey
    ) -> None:
        fingerprint = base64.b16encode(key.get_fingerprint()).decode()
        print(f"The key {fingerprint} is unknown for host {hostname}")
        res = input("Do you want to add it [y/N]? ")
        if res.upper()[:1] == "Y":
            client.get_host_keys().add(hostname, key.get_name(), key)

        else:
            raise paramiko.SSHException(f"Could not find key for {hostname!r}")


@click.command(help="Execute example paramiko command")
@click.option("-h", "--host", default="localhost", help="SSH server host")
@click.option("-p", "--port", type=int, default=2222, help="SSH server port")
@click.option("-u", "--username", default="sshuser", help="SSH user name")
@click.option("-P", "--password", default="password", help="SSH user password")
@click.option(
    "-K", "--keys", default="hostkeys", show_default=True, help="Host key list"
)
def main(host, port, username, password, keys):
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(AskPolicy())
    if os.path.isfile(keys):
        cli.load_host_keys(keys)

    cli.connect(host, port, username, password)

    _stdin, stdout, _stderr = cli.exec_command("ls /local")
    print(stdout.read().decode())

    cli.save_host_keys(keys)


if __name__ == "__main__":
    exit(main())
