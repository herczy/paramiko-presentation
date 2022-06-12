#!/usr/bin/env python3.10

"""
List all files in a given directory on the host.
"""
import datetime
import os.path
import stat

import click
import paramiko


def rwx(n, suid, sticky=False):
    if suid:
        suid = 2

    out = "-r"[n >> 2] + "-w"[(n >> 1) & 1]
    if sticky:
        out += "-xTt"[suid + (n & 1)]

    else:
        out += "-xSs"[suid + (n & 1)]

    return out


def modestr(st) -> str:
    kind = stat.S_IFMT(st.st_mode)
    if kind == stat.S_IFIFO:
        mode = "p"

    elif kind == stat.S_IFCHR:
        mode = "c"

    elif kind == stat.S_IFDIR:
        mode = "d"

    elif kind == stat.S_IFBLK:
        mode = "b"

    elif kind == stat.S_IFREG:
        mode = "-"

    elif kind == stat.S_IFLNK:
        mode = "l"

    elif kind == stat.S_IFSOCK:
        mode = "s"

    else:
        mode = "?"

    mode += rwx((st.st_mode & 0o700) >> 6, st.st_mode & stat.S_ISUID)
    mode += rwx((st.st_mode & 0o070) >> 3, st.st_mode & stat.S_ISGID)
    mode += rwx(st.st_mode & 0o007, st.st_mode & stat.S_ISVTX, True)

    return mode


@click.command(help="Execute example paramiko command")
@click.option("-h", "--host", default="localhost", help="SSH server host")
@click.option("-p", "--port", type=int, default=2222, help="SSH server port")
@click.option("-u", "--username", default="sshuser", help="SSH user name")
@click.option("-P", "--password", default="password", help="SSH user password")
@click.argument("path")
def main(host, port, username, password, path):
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect(host, port, username, password)

    sftp = cli.open_sftp()

    for name in sftp.listdir(path):
        full = os.path.join(path, name)
        mode = sftp.stat(full)
        mtime = datetime.datetime.fromtimestamp(mode.st_mtime)

        print(
            f"{modestr(mode)}   {name:30s}   uid:{mode.st_uid: 5d}   gid:{mode.st_gid: 5d}   mtime:{mtime}"
        )


if __name__ == "__main__":
    exit(main())
