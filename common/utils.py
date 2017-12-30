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
import humanize
from termcolor import colored
from functools import wraps
import pathlib


def listify(arg):
    return arg if type(arg) is list else [arg]


def generate_output_name(basename, timestamp):
    return basename+'_'+timestamp.isoformat().replace(':', '-')


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


def garbage_collect(dest, max_history, simulate=False, **kwargs):
    files = sorted(os.listdir(dest))
    f_count = len(files)
    max_history = int(max_history)
    files_to_delete = []
    if f_count > max_history:
        files_to_delete = files[:(f_count-max_history)]
        if simulate:
            print(colored("Simulation mode", 'green') + ": " + colored("GC: should remove:", 'red') + str(files_to_delete))
        else:
            for file in files_to_delete:
                os.remove(os.path.join(dest,file))
    return files_to_delete


class ModuleOutput:
    def __init__(self, output, status, file_size=0):
        self.output = output
        self.status = status
        if os.path.isfile(output):
            self.file_size = os.stat(output).st_size
        else:
            self.file_size = 0

    def generate_html(self, html_template, name):
        status = html_template.html_success if self.status else html_template.html_fail
        return html_template.html_backup_step.format(name=name,
                                                     output=self.output,
                                                     status=status,
                                                     size=humanize.filesize.naturalsize(self.file_size))


def build_dest(extension):
    def build_dest_decorator(func):
        @wraps(func)
        def func_wrapper(dest, basename, *args, **kwargs):
            pathlib.Path(dest).mkdir(parents=True, exist_ok=True)
            timestamp = datetime.datetime.now()
            kwargs['dest'] = generate_output_name(dest+'/'+basename, timestamp) + extension
            kwargs['timestamp'] = timestamp
            try:
                out = func(**kwargs)
            except:
                out = ModuleOutput(output="None", status=False)
            return out
        return func_wrapper
    return build_dest_decorator
