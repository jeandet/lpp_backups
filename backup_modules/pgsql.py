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
    type = pgsql
    dest = /some_path/backups/db
    max_history = 10
    dbmane = mydb
"""

from common import utils

@utils.build_dest('.pgsql')
def backup(dest, max_history, dbmane, user='postgres', simulate=False, *args, **kwargs):
    utils.invoke('su',['-c', 'pg_dump {}'.format(dbmane), 'postgres'], output=dest, simulate=simulate)
