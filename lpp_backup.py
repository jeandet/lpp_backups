#!/usr/bin/env python3

__author__ = "Alexis Jeandet"
__copyright__ = "Copyright 2017, Laboratory of Plasma Physics"
__credits__ = []
__license__ = "GPLv2"
__version__ = "1.0.0"
__maintainer__ = "Alexis Jeandet"
__email__ = "alexis.jeandet@member.fsf.org"
__status__ = "Development"

import importlib
import datetime
import traceback
import os
import sys
import time
import argparse
import smtplib
import configparser
from  common import mail

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--config-file", help="config file", default='~/.lpp_backup.conf')
parser.add_argument("--list-modules", help="lists available modules", action="store_true")
parser.add_argument("--sim", help="Simulation mode, just print commands", action="store_true")
args = parser.parse_args()


def print_modules():
    modules_files = [f for f in os.listdir('./backup_modules/') if f[-3:] == '.py' and f != '__init__.py']
    for m_file in modules_files:
        mod = importlib.import_module("backup_modules." + m_file[:-3], "*")
        print("- {}, {}.".format(mod.__MOD_NAME__, mod.__MOD_DESC__))


if __name__ == '__main__':

    if args.list_modules:
        print_modules()
        exit(0)

    config = configparser.ConfigParser()
    config.read(args.config_file)

    tasks = dict(config)
    tasks.pop('mail')
    tasks.pop('DEFAULT')
    for task, task_conf in tasks.items():
        module = task_conf['type']
        print("task name: {}".format(task))
        print("task type: {}".format(module))
        try:
            mod = importlib.import_module("backup_modules." + module, "*")
            mod.backup(simulate=args.sim, **task_conf)
        except:
            print(traceback.format_exc())



