#!/usr/bin/env python

import argparse
import json
import pkg_resources

from .utils.custom_errors import JSONConfigurationException, ArgumentException
from .vm_tasks import deallocate
from .vm_tasks import get_status
from .vm_tasks import turn_off
from .vm_tasks import turn_on

class ICANN(dict):

    def __init__(self, use_config_file=True):
        super(ICANN, self).__init__()

        # supported actions to take on VMs
        self['actions'] = (
            'turnon',
            'turnoff',
            'deallocate',
            'getstatus'
        )

        # action mappings
        self['action_mappings'] = {
            'turnon' : turn_on.boot,
            'turnoff' : turn_off.shut_down,
            'deallocate' : deallocate.deallocate,
            'getstatus' : get_status.status,
        }

        # either use the config file or manually insert the nicknames you want to give your remote hosts.
        if use_config_file is True:
            try:
                # TODO: NICE LIST-COMPREHENSIONS DAWG. THEY WORK?
                config_dict = json.load(pkg_resources.resource_stream('config', 'host_config.json'))
                self['host_nicknames'] = tuple([host_record['cmdline_hostname'] for host_record in config_dict.get('hosts')])
                self['host_realnames'] = tuple([host_record['azure_hostname'] for host_record in config_dict.get('hosts')])
                self['host_mappings'] = dict(zip(self['host_nicknames'], self['host_realnames']))
                self['resource_group'] = config_dict.get('resource_group')
            except Exception:
                raise JSONConfigurationException('There was an error while parsing your host_config.json file.')
        # Note that if the config file isn't used, the `host_X` values are designated in reverse order.
        # I can't think of a potential issue with this, but when has anyone thought of actual potential issues.
        else:
            # DEFINE CMDLINE-HOSTNAMES HERE IF YOU DON'T WANT TO USE THE CONFIG FILE.
            # KEYS == CMDLINE VM-NAMES/SHORTHAND; VALUES == VM-NAME DESIGNATED ON AZURE.
            self['host_mappings'] = {
                'loc': 'localhost',
                # 'example' : 'exampleHostMachine',
            }
            self['host_realnames'] = self['host_mappings'].values()
            self['host_nicknames'] = self['host_mappings'].keys()
            self['resource_group'] = 'ExactRGNameAsAppearsOnAzure'

            # Hopefully this overrides stuff.


    def __setattr__(self, key=None, value=None):
        pass


# validate that there aren't any conflicting arguments
def __validate_args(args):
    if args.json_credentials and args.infile_credentials:
        raise ArgumentException('You can only use one credential format at a time.')

    if args.wait and args.force:
        print 'WARNING: You have specified both --wait & --force. Note that --force takes precedence. \nContinuing.'


# validate that the command is a legal one.
def __validate_command(action=None, host=None):
    if action is None or host is None:
        raise argparse.ArgumentError(argument=action, message='you must supply both an action & a host')

    validator = ICANN()

    assert action in validator['actions'], 'Action name error. Try azureutils --help.'
    assert host in validator['host_nicknames'], 'Host name error. Try azureutils --help.'

    pass


def main(args=None):
    if args is None:
        parser = argparse.ArgumentParser()
        parser.add_argument('action', nargs="?", help='options are <turnon|turnoff|deallocate>')
        parser.add_argument('host', nargs="?", help='select a host options are <trump|bernie|kali>')
        parser.add_argument('-C', '--json-credentials', action='store_true', default=False, help="use the internal PLAINTEXT config file, 'credentials_config.json', for Azure credentials. Default is False 'cuz this is dangerous if you don't read & follow the WARNING.txt file.")
        parser.add_argument('-i', '--infile-credentials', nargs="?", type=argparse.FileType('r'), default=None, help="pass in a text file containing your credentials. See example_credfile.txt for format")
        parser.add_argument('-w', '--wait', action='store_true', help="Wait for your vm to do whatever. Default true for applicable operations.")
        parser.add_argument('-f', '--force', action='store_true', help="Don't wait for vm's to be done doing things. Overrides -w.")

        arrgs = parser.parse_args()

        # input validations.
        __validate_args(arrgs)
        __validate_command(action=arrgs.action, host=arrgs.host)

        # handle force/wait
        if arrgs.force:
            wait = 'false'
        elif arrgs.wait:
            assert str(arrgs.wait.lower()) in ('true', 'false'), 'value for <-w|--wait> must be <[true]|false>'
            wait = str(arrgs.wait.lower())
        else:
            wait = 'true'

        # handle credential-type
        if arrgs.json_credentials:
            # This loads the data-files using the 'config' keyword defined in setup.py
            cred_dict = json.load(pkg_resources.resource_stream('config', 'credentials_config.json'))
            creds = (cred_dict['tenant_id'], cred_dict['client_id'], cred_dict['secret'])
        elif arrgs.infile:
            creds = arrgs.infile
        else:
            print 'WARNING: Credentials have not been passed in.\n You will need to enter them by hand.\n\n'
            creds = None

        # This is mostly a sanity check. 
        # `wait` should be a bool & `creds` can be a filepath (aka a string), tuple, or NoneType.
        # regardless, they should both be defined by now. If this assert statement pops-off, thar B issues.
        assert wait and (creds or creds is None), 'argument error.'

        action_input, host_input = arrgs.action, arrgs.host

        # This is what it's all about right hurrrrr:
        function_to_use = ICANN()['action_mappings'][action_input]
        real_hostname = ICANN()['host_mappings'][host_input]
        rg = ICANN()['resource_group']

        # aaaaaaaaand GO!
        if wait == 'false':
            function_to_use(creds, resource_group=rg, vm=real_hostname, wait=False)
        else:
            function_to_use(creds, resource_group=rg, vm=real_hostname)

    else: exit(1)

if __name__ == '__main__':
    main()
