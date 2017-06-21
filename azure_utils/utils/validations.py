import argparse

from azure_utils.__main__ import ICANN
from azure_utils.utils.custom_errors import ArgumentException


def __validate_args(args):
    if args.json_credentials and args.infile_credentials:
        raise ArgumentException('You can only use one credential format at a time.')

    if args.wait and args.force:
        print 'WARNING: You have specified both --wait & --force. Note that --force takes precedence. \nContinuing.'


def __validate_command(action=None, host=None):
    if action is None or host is None:
        raise argparse.ArgumentError(argument=action, message='you must supply both an action & a host')

    validator = ICANN()

    assert action in validator['actions'], 'Action name error. Try azureutils --help.'
    assert host in validator['host_nicknames'], 'Host name error. Try azureutils --help.'

    pass