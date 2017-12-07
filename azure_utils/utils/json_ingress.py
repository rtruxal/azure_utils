import json
import os
import pkg_resources

from azure_utils.utils.custom_errors import JSONInfileParsingException, JSONInfileConfigException, ArgumentException, \
    READ_THE_DAMN_WARNING_FILE, RTDWFITDD_messages

from azure_utils import get_data


# def main():
#     from azure_utils import get_data
#     print get_data('config/host_config.json')
#     print os.path.exists(get_data('config/host_config.json'))
#     with open(get_data('config/host_config.json'), 'r') as jsonconfig:
#         print json.load(jsonconfig)
#
# if __name__ == '__main__':
#     main()


def load_sub_id(default=True, alt=None):
    #TODO: Well I figured out how to do this for the other 2. Fix.
    if default is True:
        # import pdb
        # pdb.set_trace()
        json_pth = get_data('config/host_config.json')
        try:
            with open(json_pth, 'r') as jsonfile:
                return str(json.load(jsonfile).get('subscription_id'))
        except Exception:
            try:
                return str(json.load(pkg_resources.resource_stream('data', 'host_config.json')).get('subscription_id'))
            except Exception:
                raise JSONInfileParsingException('your subscription ID could not be parsed out of host_config.json')
    # this only checks if alt is a string. Prly should have some more checks.
    elif alt is not None and isinstance(alt, str):
        try:
            assert os.path.exists(get_data('config/{}'.format(alt)))
        except AssertionError:
            raise JSONInfileConfigException('the data filename passed to `alt` is malformed or not present.')
        try:
            with open(get_data('config/{}'.format(alt)), 'r') as jsonfile:
                return str(json.load(jsonfile).get('subscription_id'))
        except Exception:
            try:
                return str(json.load(pkg_resources.resource_stream('data', alt)).get('subscription_id'))
            except Exception:
                raise JSONInfileParsingException('your subscription ID could not be parsed out of host_config.json')
    else: raise ArgumentException('see `azure_utils.utils.subscription_id_file.load_sub_id.__doc__` for usage.')


def load_host_creds(alt_infile=None):
    # K so now we gonna try to deal with the input JSON.
    # including non-.py "config" files within a python package has 2 flavors: binary-install & sdist compilation.
    # thus the semi-excessive try/except statements.
    from azure_utils import get_data

    if alt_infile is not None:
        assert os.path.exists(os.path.realpath(alt_infile)) and os.path.isfile(alt_infile), \
            'An INVALID alternate JSON config-file path was passed. Please check your host_config.json analog.'
        infile_pth = os.path.realpath(alt_infile)
    else:
        infile_pth = get_data('config/credentials_config.json')

    try:
        # This uses the function `get_data()` from the top-level __init__.py file.
        with open(infile_pth, 'r') as jsonfile:
            cred_dict = json.load(jsonfile)
    except Exception:
        # This loads the config-files using the 'data' keyword defined in setup.py
        cred_dict = json.load(pkg_resources.resource_stream('data', 'credentials_config.json'))
    finally:
        del get_data

    # Check if warnings have been read.
    # No but srsly.
    if cred_dict.get('have_read_warning') == False:
        #than we haven't changed the credfile man.
        raise READ_THE_DAMN_WARNING_FILE(RTDWFITDD_messages.read_warning_false())
    elif cred_dict.get('have_read_warning') == True:
        # someone changed the credfile without reading the warning!
        raise READ_THE_DAMN_WARNING_FILE(RTDWFITDD_messages.read_warning_true())
    elif cred_dict.get('have_read_warning') is not None:
        # same as above but lord knows what they put in there.
        raise JSONInfileConfigException(RTDWFITDD_messages.read_warning_true())

    return cred_dict


def load_host_config(alt_infile=None):
    from azure_utils import get_data

    if alt_infile is not None:
        assert os.path.exists(os.path.realpath(alt_infile)) and os.path.isfile(alt_infile), \
            'An INVALID alternate JSON config-file path was passed. Please check your host_config.json analog.'
        infile_pth = os.path.realpath(alt_infile)
    else:
        infile_pth = get_data('config/host_config.json')

    try:
        # for a source install.
        with open(infile_pth, 'r') as jsonfile:
            config_dict = json.load(jsonfile)
    except Exception:
        # for a binary install.
        config_dict = json.load(pkg_resources.resource_stream('data', 'host_config.json'))
    finally:
        del get_data

    return config_dict