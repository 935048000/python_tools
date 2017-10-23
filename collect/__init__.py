import sys
from collect.aep import collect
from collect.txt2excel import dataswitch
from collect.pgsql import pgsql
from collect.version import __version__

#python version > V2.6
if sys.version_info < (2, 6):
    raise RuntimeError('You need Python 2.6+ for this module.')

__author__ = "chen.hao <chenhao159482@gmail.com>"
__license__ = "GNU Lesser General Public License (LGPL)"


__all__ = ['collect','dataswitch','pgsql','__version__',]