import os
#TODO: Y DO I NEED GLOBAL VARIABLES IN MY INIT FILE?!?!!?!?!?!??!
def get_data(path):
    _ROOT = os.path.abspath(os.path.dirname(__file__))
    return os.path.realpath(os.path.join(_ROOT, 'config', path))
def put_logs(log_id='default'):
    _ROOT = os.path.abspath(os.path.dirname(__file__))
    return os.path.realpath(os.path.join(_ROOT, 'config', 'logs/logfile_{}.log'.format(log_id)))

import vm_tasks
import core
import utils

# NO. BAD WILDCARDS.
__all__ = [
    'utils',
    'compute_tasks',
    'core',
]
