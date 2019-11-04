#!/usr/bin/env python3
import os
from argparse import ArgumentParser
from time import sleep


def get_arguments():
    parser = ArgumentParser(
        description="Use this script to create a tiny agent that will periodically rerun your --cmd command, "
                    "so you won't lose your shell anymore.")
    parser.add_argument('--sleep',
                        dest='sleep',
                        required=True,
                        help='Sleep timer in seconds. This timer specifies how often the given --cmd command runs. '
                             '60 == 1min, 3600 == 1hour')
    parser.add_argument('--cmd',
                        dest='cmd',
                        required=True,
                        help='Command to use, in the following format: '
                             '"C:\\WINDOWS\\system32\\backdoor.exe"')
    options = parser.parse_args()
    return options


def execute_command(cmd):
    try:
        os.system(cmd)
    except Exception as e:
        print(e)


def work(cmd, sleep_timer_in_seconds):
    while True:
        print('Running [{cmd}]'.format(cmd=cmd))
        execute_command(cmd)
        print('Sleeping for {sleep} seconds'.format(sleep=sleep_timer_in_seconds))
        sleep(sleep_timer_in_seconds)


options = get_arguments()
work(options.cmd, int(options.sleep))
