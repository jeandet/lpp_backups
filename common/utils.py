#!/usr/bin/env python3

__author__ = "Alexis Jeandet"
__copyright__ = "Copyright 2017, Laboratory of Plasma Physics"
__credits__ = []
__license__ = "GPLv2"
__version__ = "1.0.0"
__maintainer__ = "Alexis Jeandet"
__email__ = "alexis.jeandet@member.fsf.org"
__status__ = "Development"

import subprocess
import datetime
from termcolor import colored
from functools import wraps


def listify(arg):
    return arg if type(arg) is list else [arg]


def generate_output_name(basename, timestamp):
    return basename+'_'+timestamp.isoformat()


def build_dest(extension):
    def build_dest_decorator(func):
        @wraps(func)
        def func_wrapper(dest, *args, **kwargs):
            timestamp = datetime.datetime.now()
            kwargs['dest'] = generate_output_name(dest, timestamp) + extension
            kwargs['timestamp'] = timestamp
            return func(**kwargs)
        return func_wrapper
    return build_dest_decorator


def invoke(command, args, output=None, simulate=False):
    cmd = listify(command) + listify(args)

    if simulate:
        output = "" if output is None else " > "+str(output)
        print(colored("Simulation mode",'green')+ ": " + colored(" ".join(cmd) + output, 'red'))
        return None

    if type(output) is str:
        output = open(output, 'w')

    p = subprocess.run(cmd, stdout=output, stderr=subprocess.PIPE)
    return p


def find_program(program):
    p = invoke('which', program, output=subprocess.PIPE)
    if p.returncode == 0:
        return p.stdout
    else:
        return None
