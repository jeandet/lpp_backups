#!/usr/bin/env python3

__author__ = "Alexis Jeandet"
__copyright__ = "Copyright 2017, Laboratory of Plasma Physics"
__credits__ = []
__license__ = "GPLv2"
__version__ = "1.0.0"
__maintainer__ = "Alexis Jeandet"
__email__ = "alexis.jeandet@member.fsf.org"
__status__ = "Development"


__MOD_NAME__="Folder(folder)"

__MOD_DESC__ = "performs backups of given folder"

__MOD_SAMPLE_CONFIG__ = """
    Sample config:
    ------------------------------------------------------------------
    [my-folder]
    type = folder
    dest = /some_path/backups/
    max_history = 10
    path = /some_path/folder_to_backup
"""


from common import utils


@utils.build_dest('.zip')
def backup(source, dest, max_history, timestamp, simulate=False, *args, **kwargs):
    utils.invoke('pigz',['-r', dest, source], simulate=simulate)
