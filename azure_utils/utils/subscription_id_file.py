import json
import pkg_resources
from custom_errors import ArgumentException

def load_sub_id(default=True, alt=None):
    """
    This function loads the subscription ID listed in config/host_config.json by default.

    If you rename the config-file, set `default` to False & pass the new filename via the `alt` arg.
    :param default: [True|False] -- set to False to use the `alt` arg.
    :param alt: type str -- alternate name for your JSON config-file.
    :return: type str -- your subscription-id.
    """
    if default is True:
        return json.load(pkg_resources.resource_stream('config', 'host_config.json')).get('subscription_id')
    # this only checks if alt is a string. Prly should have some more checks.
    elif alt is not None and isinstance(alt, str):
        return json.load(pkg_resources.resource_stream('config', alt)).get('subscription_id')
    else: raise ArgumentException('see `azure_utils.utils.subscription_id_file.load_sub_id.__doc__` for usage.')
