# pwntty

Pwntty is an open source project to control other terminals on your machine. Mainly focused on real time CTF games (KoTH, Battlegrounds, etc), pwntty has several features for fun.

Installation
----

Download pwntty by cloning the [Git](https://github.com/exnorz/pwntty.git) repository:
```
git clone https://github.com/exnorz/pwntty pwntty
```

Usage
----

To get a list of basic options use:
```
# python pwntty.py -h
```

Some of pwntty options:
```
usage: pwntty [-h] -d PATH [PATH ...] [-e [COMMAND]] [-m [MESSAGE]]
              [-b [CURSOR]] [-l [LOCK_TTY]]

A toolkit to control TTY devices

options:
  -h, --help            show this help message and exit
  -d PATH [PATH ...], --devices PATH [PATH ...]
                        Target TTY device
  -e [COMMAND], --exec [COMMAND]
                        Run a given command line on TTY
  -m [MESSAGE], --message [MESSAGE]
                        Write a message to TTY
  -b [CURSOR], --bug-cursor [CURSOR]
                        Turn on the bug cursor on TTY
  -l [LOCK_TTY], --lock-tty [LOCK_TTY]
                        Lock the TTY I/O
```

Requirements
----
- Python3.0+

# License
MIT License

Copyright (c) 2022 Ricardo Costa
