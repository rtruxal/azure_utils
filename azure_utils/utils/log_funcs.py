from time import asctime
import logging


def log_level_info(f):
    logging.basicConfig(filename='{}.log'.format(__name__), level=logging.INFO)
    def wrapper(*args, **kwargs):
        logging.info(
            '{}\tThe func: "{}" Ran with args: "{}" and with kwargs: "{}"'.format(asctime(), f.__name__, args, kwargs)
        )
        return f(*args, **kwargs)
    return wrapper