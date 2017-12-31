#!/usr/bin/env python3

from setuptools import setup

setup(name='lpp_backups',
      version='0.1',
      description='LPP\'s backup system',
      url='https://github.com/jeandet/lpp_backups',
      author='Alexis Jeandet',
      author_email='alexis.jeandet@member.fsf.org',
      license='GPLv2+',
      packages=['common', 'backup', 'monitor'],
      install_requires=[
            'argparse',
            'configparser',
            'datetime',
            'humanize',
            'termcolor',
            'pathlib',
            'email',
            'psutil'
      ],
      zip_safe=False,
      scripts=['lpp_backup'],
      )
