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


def invoke(command, args, stdout=None, stdin=None, simulate=False):
    cmd = listify(command) + listify(args)

    if simulate:
        stdout = "" if stdout is None else " > " + str(stdout)
        stdin = "" if stdin is None else " < " + str(stdin)
        print(colored("Simulation mode",'green') + ": " + colored(" ".join(cmd) + stdin + stdout, 'red'))
        return subprocess.run('true', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if type(stdout) is str:
        stdout = open(stdout, 'w')
    if type(stdin) is str:
        stdin = open(stdin, 'w')

    p = subprocess.run(cmd, stdout=stdout, stdin=stdin, stderr=subprocess.PIPE)
    return p


def find_program(program):
    p = invoke('which', program, stdout=subprocess.PIPE)
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
    def __init__(self, output, status, task_name, file_size=0, **kwargs):
        self.output = output
        self.status = status
        self.task_name = task_name
        if os.path.isfile(output):
            self.file_size = os.stat(output).st_size
        else:
            self.file_size = 0

    def generate_html(self, html_template):
        status = html_template.html_success if self.status else html_template.html_fail
        return html_template.html_backup_step.format(name=self.task_name,
                                                     output=self.output,
                                                     status=status,
                                                     size=humanize.filesize.naturalsize(self.file_size))


class MonitorOutput:
    def __init__(self, path, usage, free, available, task_name, **kwargs):
        self.usage = usage
        self.path = path
        self.free = free
        self.available = available
        self.task_name = task_name

    def generate_html(self, html_template):
        return html_template.html_monitor_element.format(name=self.task_name + " " + self.path,
                                                         usage=humanize.filesize.naturalsize(self.usage),
                                                         available=humanize.filesize.naturalsize(self.available),
                                                         free=humanize.filesize.naturalsize(self.free))


def build_dest(extension):
    def build_dest_decorator(func):
        @wraps(func)
        def func_wrapper(dest, task_name, *args, **kwargs):
            pathlib.Path(dest).mkdir(parents=True, exist_ok=True)
            timestamp = datetime.datetime.now()
            kwargs['dest'] = generate_output_name(dest+'/'+task_name, timestamp) + extension
            kwargs['timestamp'] = timestamp
            kwargs['task_name'] = task_name
            try:
                out = func(**kwargs)
            except:
                out = ModuleOutput(output="None", status=False, **kwargs)
            return out
        return func_wrapper
    return build_dest_decorator
