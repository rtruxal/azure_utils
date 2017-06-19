import json
import os

import pkg_resources

from azure_utils.utils.custom_errors import JSONInfileParsingException, JSONInfileConfigException, ArgumentException
from azure_utils import get_data


# def main():
#     from azure_utils import get_data
#     print get_data('data/host_config.json')
#     print os.path.exists(get_data('data/host_config.json'))
#     with open(get_data('data/host_config.json'), 'r') as jsonconfig:
#         print json.load(jsonconfig)
#
# if __name__ == '__main__':
#     main()


def load_sub_id(default=True, alt=None):
    # import pdb
    # pdb.set_trace()
    """
    This function loads the subscription ID listed in config/host_config.json by default.

    Why this function is so messy:
     - Including non *.py files inside of distributable python packages is a SERIOUS pain in the "you-know-what."
     - There are 2 extraction methods used below; one works with pip's sdist, and the other works with a binary install.
     - (Note the nested try/except statements inside the if/elif blocks.)

    If you rename the config-file, set `default` to False & pass the new filename via the `alt` arg.
    :param default: [True|False] -- set to False to use the `alt` arg.
    :param alt: type str -- alternate name for your JSON config-file.
    :return: type str -- your subscription-id.
    """
    if default is True:
        try:
            with open(get_data('data/host_config.json'), 'r') as jsonfile:
                return str(json.load(jsonfile).get('subscription_id'))
        except Exception:
            try:
                return str(json.load(pkg_resources.resource_stream('config', 'host_config.json')).get('subscription_id'))
            except Exception:
                raise JSONInfileParsingException('your subscription ID could not be parsed out of host_config.json')
    # this only checks if alt is a string. Prly should have some more checks.
    elif alt is not None and isinstance(alt, str):
        try:
            assert os.path.exists(get_data('data/{}'.format(alt)))
        except AssertionError:
            raise JSONInfileConfigException('the config filename passed to `alt` is malformed or not present.')
        try:
            with open(get_data('data/{}'.format(alt)), 'r') as jsonfile:
                return str(json.load(jsonfile).get('subscription_id'))
        except Exception:
            try:
                return str(json.load(pkg_resources.resource_stream('config', alt)).get('subscription_id'))
            except Exception:
                raise JSONInfileParsingException('your subscription ID could not be parsed out of host_config.json')
    else: raise ArgumentException('see `azure_utils.utils.subscription_id_file.load_sub_id.__doc__` for usage.')