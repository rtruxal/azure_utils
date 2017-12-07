from time import asctime
import logging
from azure_utils import put_logs

import functools

def INFO_log_args(f):
    try:
        logging.basicConfig(filename=put_logs(asctime()[4:10]), level=logging.INFO)
    except Exception:
        logging.basicConfig(filename=put_logs(), level=logging.INFO)

    def wrapper(*args, **kwargs):
        logging.info(
            '{}\tThe func: "{}" Ran with args: "{}" and with kwargs: "{}"'.format(asctime(), f.__name__, args, kwargs)
        )
        return f(*args, **kwargs)
    return wrapper


def INFO_expected_exception(f):
    """
    A decorator that wraps the passed in f and logs
    exceptions should one occur
    """
    try:
        logging.basicConfig(filename=put_logs(asctime()[4:10]), level=logging.INFO)
    except Exception:
        logging.basicConfig(filename=put_logs(), level=logging.INFO)

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            logging.exception(
                '{}\tThe func: "{}" handled an expected exception:'.format(asctime(), f.__name__)
            )
            return f(*args, **kwargs)

    return wrapper

def WARN_unexpected_exception(f):
    """
    A decorator that wraps the passed in f and logs
    exceptions should one occur
    """
    try:
        logging.basicConfig(filename=put_logs(asctime()[4:10]), level=logging.WARN)
    except Exception:
        logging.basicConfig(filename=put_logs(), level=logging.WARN)

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            logging.exception(
                '{}\tThe func: "{}" handled an unexpected exception'.format(asctime(), f.__name__)
            )
            return f(*args, **kwargs)

    return wrapper