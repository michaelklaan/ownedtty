#!/usr/bin/env python3

from random import randint
from termios import TIOCSTI
from time import sleep

import argparse
import fcntl
import os
import sys

banner = r'''
                  .         *    .            *          .----. .
 '  ____               ______________  __    .---------. | == |
   / __ \_    " ______/_  __/_  __/\ \/ /    |.-"""""-.| |----|  
  / /_/ / | /| / / __ \/ /   / /    \  /     ||       || | == |   
 / ____/| |/ |/ / / / / /   / / ,   / / *    ||       || |----|
/_/     |__/|__/_/ /_/_/   /_/     /_/       |'-.....-'| |::::|
,                                            `"")---(""` |____|
    Version 1.0 | Created by @exnorz        /:::::::::::\" \'\                                  
'''

print(banner, file=sys.stderr)

def parse_args():
    parser = argparse.ArgumentParser(
        prog="pwntty",
        description="A toolkit to control TTY devices")

    parser.add_argument(
        "-d", "--devices",
        nargs="+",
        required=True,
        help="Target TTY device",
        metavar="PATH")

    parser.add_argument(
        "-e", "--exec",
        nargs="?",
        help="Run a given command line on TTY",
        metavar="COMMAND"
    )

    parser.add_argument(
        "-m", "--message",
        nargs="?",
        help="Write a message to TTY")

    parser.add_argument(
        "-b", "--bug-cursor",
        nargs="?",
        default="",
        help="Turn on the bug cursor on TTY",
        metavar="CURSOR"
    )

    parser.add_argument(
        "-l", "--lock-tty",
        nargs="?",
        default=False,
        help="Lock the TTY I/O")

    return parser.parse_args()


def write(dev, data):
    os.write(dev, data.encode())


def send_input(dev, data):
    for ch in data:
        fcntl.ioctl(dev, TIOCSTI, ch)


def lock_tty_io(dev):
    cmd = "exec 2>&-\nclear\nexec >&-\n"
    send_input(dev, cmd)
    write(dev, "\033[9C")


def bug_tty_cursor(dev, cur):
    codes = lambda n: f"\033[XZ".replace(
        "X", str(n)).replace("Z", list("ABCD")[randint(0, 3)])

    try:
        while True:
            write(dev, codes(randint(0, 0x7f)))
    except KeyboardInterrupt:
        print("- Bug cursor stopped (CTRL + C)", file=sys.stderr)


def main():
    args = parse_args()
    devices = []

    if not os.getuid() == 0:
        print("error: pwntty must be run as root", file=sys.stderr)
        exit(1)

    print("* Checking devices...")
    for dev in args.devices:
        try:
            fd = os.open(dev, os.O_RDWR)
            devices.append(fd)
            print(f"+ The device '{dev} is OK!")
        except Exception as e:
            print(f"- {e}", file=sys.stderr)

    if args.exec:
        for dev in devices:
            send_input(dev, args.exec + "\n")

    if args.message:
        for dev in devices:
            for ch in args.message:
                write(dev, ch)
                sleep(0.05)
            write(dev, "\n")

    if args.bug_cursor:
        for dev in devices:
            bug_tty_cursor(dev, cur=args.bug_cursor[0])

    if args.lock_tty is None:
        for dev in devices:
            lock_tty_io(dev)


if __name__ == "__main__":
    main()
