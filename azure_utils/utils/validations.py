import argparse
import os
from azure_utils.utils.custom_errors import ArgumentException, JSONInfileConfigException


def _validate_args(args):
    if args.json_credentials and args.infile_credentials:
        raise ArgumentException('You can only use one credential format at a time.')

    if args.wait and args.force:
        print 'WARNING: You have specified both --wait & --force. Note that --force takes precedence. \nContinuing.'


def _validate_command(ICANN_instance, action=None, host=None):
    if action is None or host is None:
        raise argparse.ArgumentError(argument=action, message='you must supply both an action & a host')

    validator = ICANN_instance

    assert action in validator['actions'], 'Action name error. Try azureutils --help.'
    assert host in validator['host_nicknames'], 'Host name error. Try azureutils --help.'

    pass

def _validate_infile(infile_path):
    assert isinstance(str(infile_path), str)
    try:
        assert os.path.exists(infile_path)
    except AssertionError:
        try:
            assert os.path.exists(os.path.realpath(infile_path))
        except AssertionError:
            raise JSONInfileConfigException('path provided to infile does not exist.')
