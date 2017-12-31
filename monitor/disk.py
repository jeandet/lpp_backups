#!/usr/bin/env python3

__author__ = "Alexis Jeandet"
__copyright__ = "Copyright 2017, Laboratory of Plasma Physics"
__credits__ = []
__license__ = "GPLv2"
__version__ = "1.0.0"
__maintainer__ = "Alexis Jeandet"
__email__ = "alexis.jeandet@member.fsf.org"
__status__ = "Development"


__MOD_NAME__="Disk monitor(disk)"

__MOD_DESC__ = "monitors disk usage"

__MOD_SAMPLE_CONFIG__ = """
    Sample config:
    ------------------------------------------------------------------
    [my-disk-monitor]
    type = monitor:disk
    path = /some_path_to_monitor
    max_history = 10
"""


import psutil
from common import utils


def monitor(path, simulate=False, *args, **kwargs):
    info = psutil.disk_usage(path)
    return utils.MonitorOutput(path, info.used, info.free, info.total, **kwargs)
