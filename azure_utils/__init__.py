from _version import __version__

import os
def get_data(path):
    _ROOT = os.path.abspath(os.path.dirname(__file__))
    return os.path.realpath(os.path.join(_ROOT, 'data', path))
def put_logs(log_id='default'):
    _ROOT = os.path.abspath(os.path.dirname(__file__))
    return os.path.realpath(os.path.join(_ROOT, 'data', 'logs/logfile_{}.log'.format(log_id)))

import vm_tasks
import core
import utils
import data

# NO. BAD WILDCARDS.
__all__ = [
    'utils',
    'compute_tasks',
    'core',
]
