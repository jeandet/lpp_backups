#!/usr/bin/env python3

__author__ = "Alexis Jeandet"
__copyright__ = "Copyright 2017, Laboratory of Plasma Physics"
__credits__ = []
__license__ = "GPLv2"
__version__ = "1.0.0"
__maintainer__ = "Alexis Jeandet"
__email__ = "alexis.jeandet@member.fsf.org"
__status__ = "Development"

import os
import subprocess
import datetime
from termcolor import colored
from functools import wraps
import pathlib


def listify(arg):
    return arg if type(arg) is list else [arg]


def generate_output_name(basename, timestamp):
    return basename+'_'+timestamp.isoformat().replace(':', '-')


def build_dest(extension):
    def build_dest_decorator(func):
        @wraps(func)
        def func_wrapper(dest, basename, *args, **kwargs):
            pathlib.Path(dest).mkdir(parents=True, exist_ok=True)
            timestamp = datetime.datetime.now()
            kwargs['dest'] = generate_output_name(dest+'/'+basename, timestamp) + extension
            kwargs['timestamp'] = timestamp
            return func(**kwargs)
        return func_wrapper
    return build_dest_decorator


def invoke(command, args, output=None, simulate=False):
    cmd = listify(command) + listify(args)

    if simulate:
        output = "" if output is None else " > "+str(output)
        print(colored("Simulation mode",'green')+ ": " + colored(" ".join(cmd) + output, 'red'))
        return subprocess.run('true', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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


class ModuleOutput:
    def __init__(self, output, status, file_size=0):
        self.output = output
        self.status = status
        self.file_size = os.stat(output).st_size

    def generate_html(self, html_template, name):
        status = html_template.html_success if self.status else html_template.html_fail
        return html_template.html_backup_step.format(name=name, output=self.output, status=status, size=self.file_size)
