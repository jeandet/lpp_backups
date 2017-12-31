#!/usr/bin/env python3

__author__ = "Alexis Jeandet"
__copyright__ = "Copyright 2017, Laboratory of Plasma Physics"
__credits__ = []
__license__ = "GPLv2"
__version__ = "1.0.0"
__maintainer__ = "Alexis Jeandet"
__email__ = "alexis.jeandet@member.fsf.org"
__status__ = "Development"


__MOD_NAME__="PostgreSQL(pgsql)"

__MOD_DESC__ = "performs backups on PostgreSQL databases"

__MOD_SAMPLE_CONFIG__ = """
    Sample config:
    ------------------------------------------------------------------
    [my-database]
    type = mysql
    dest = /some_path/backups/db
    max_history = 10
    dbmane = mydb
    user = db_user
    host = some_host
"""

import tempfile
import os
from common import utils

@utils.build_dest('.sql.tar.gz')
def backup(dest, max_history, dbmane, timestamp, user='postgres', simulate=False, *args, **kwargs):
    status = False
    print(kwargs)
    my_args = []
    if "host" in kwargs:
        my_args += ["-h"] + [kwargs["host"]]
    my_args += ["-u"] + [user]
    my_args.append(dbmane)
    with open(dest[:-7], "w") as fp:
        p = utils.invoke('mysqldump', my_args, stdout=fp, simulate=simulate)
        fp.flush()
        p2 = utils.invoke('tar', ['-c', '--use-compress-program=pigz', '-f', dest, fp.name], simulate=simulate)
        status = (p.returncode == 0) & (p2.returncode == 0)
    os.remove(dest[:-7])
    return utils.ModuleOutput(output=dest, status=status, **kwargs)

