#!/usr/bin/env python3.10

"""
Copy files from host
"""

import click
import paramiko


@click.command(help="Execute example paramiko command")
@click.option("-h", "--host", default="localhost", help="SSH server host")
@click.option("-p", "--port", type=int, default=2222, help="SSH server port")
@click.option("-u", "--username", default="sshuser", help="SSH user name")
@click.option("-P", "--password", default="password", help="SSH user password")
@click.argument("source")
@click.argument("target")
def main(host, port, username, password, source, target):
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(host, port, username, password)

    sftp = cli.open_sftp()

    sftp.get(source, target)


if __name__ == "__main__":
    exit(main())
