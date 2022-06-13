#!/usr/bin/env python3.10

"""
Execute a single command on the given SSH server
"""

import click
import paramiko


@click.command(help="Execute example paramiko command")
@click.option("-h", "--host", default="localhost", help="SSH server host")
@click.option("-p", "--port", type=int, default=2222, help="SSH server port")
@click.option("-u", "--username", default="sshuser", help="SSH user name")
@click.option("-P", "--password", default="password", help="SSH user password")
@click.argument("command")
@click.argument("args", nargs=-1)
def main(host, port, username, password, command, args):
    # Create the SSH client object
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(host, port, username, password)

    # Execute the command
    stdin, stdout, stderr = cli.exec_command(" ".join([command, *args]))

    # Print the results
    print("STDOUT:")
    print(stdout.read().decode())

    print("STDERR:")
    print(stderr.read().decode())

    print("Return code:", stdout.channel.recv_exit_status())


if __name__ == "__main__":
    exit(main())
