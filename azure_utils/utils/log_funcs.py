from time import asctime
import logging
from azure_utils import put_logs

def log_level_info(f):
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