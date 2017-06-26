#!/usr/bin/env python

import argparse

from _version import __version__

from azure_utils.utils.custom_errors import JSONInfileConfigException
from azure_utils.utils.json_ingress import load_host_creds, load_host_config
from azure_utils.utils.validations import _validate_args, _validate_command
from azure_utils.vm_tasks import deallocate
from azure_utils.vm_tasks import get_status
from azure_utils.vm_tasks import turn_off
from azure_utils.vm_tasks import turn_on


class ICANN(dict):
    def __init__(self, use_json_config=True, alt_config_file=None):
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

        # either use the data file or manually insert the nicknames you want to give your remote hosts.
        if use_json_config is True:
            config_dict = load_host_config(alt_infile=alt_config_file)
            try: #...a bunch of list comprehensions.
                self['host_resource_groups'] = tuple([host_record['resource_group'] for host_record in config_dict.get('hosts')])
                self['host_nicknames'] = tuple([host_record['cmdline_hostname'] for host_record in config_dict.get('hosts')])
                self['host_realnames'] = tuple([host_record['azure_hostname'] for host_record in config_dict.get('hosts')])
                self['host_mappings'] = dict(zip(self['host_nicknames'], zip(self['host_resource_groups'], self['host_realnames'])))
                self['default_resource_group'] = config_dict.get('default_resource_group')
            except Exception:
                raise JSONInfileConfigException('There was an error while parsing your host_config.json file.')

        # Note that if the data file isn't used, the `host_X` values are designated in reverse order.
        # I can't think of a potential issue with this, but when has anyone thought of actual potential issues.
        else:
            self['default_resource_group'] = 'Specify-ExactRGNameAsItAppearsOnAzure'

            # IF YOU DON'T WANT TO USE THE CONFIG FILE,
            # DEFINE CMDLINE-HOSTNAMES & RESOURCE GROUPS BELOW.
            self['host_mappings'] = {
                'loc': ('localhostResourceGroup','localhost'), # <--this is useless.
            }

            self['host_resource_groups'] = [valtuple[0] for valtuple in self['host_mappings'].values()]
            self['host_realnames'] = [valtuple[1] for valtuple in self['host_mappings'].values()]
            self['host_nicknames'] = self['host_mappings'].keys()



    def print_state(self):
        for attribute in [k for k, v in self.__dict__ if v]:
            print '{}:  {}\n'.format(attribute, self.__dict__[attribute])

    # Hopefully this overrides stuff.
    def __setattr__(self, key=None, value=None):
        pass


def main(args=None):
    if args is None:
        #TODO: lil' more coherence to these options.
        parser = argparse.ArgumentParser()
        parser.add_argument('action', nargs="?", help='options are <turnon|turnoff|deallocate>')
        parser.add_argument('host', nargs="?", help='select a host using `cmdline_hostname` from azure_utils/data/config/host_config.json <foo_host_1|foo_host_2|etc...>')
        parser.add_argument('-j', '--json-credentials', action='store_true', default=False, help="use the internal PLAINTEXT data file, 'credentials_config.json', for Azure credentials. Default is False 'cuz this is dangerous if you don't read & follow the WARNING.txt file.")
        parser.add_argument('-J', '--json-infile-credentials', nargs="?", type=argparse.FileType('r'), default=None, help="pass in a JSON file-path containing your credentials. See credentials_config.json for format.")
        parser.add_argument('-i', '--infile-credentials', nargs="?", type=argparse.FileType('r'), default=None, help="pass in a text file-path containing your credentials. See example_credfile.txt for format.")
        parser.add_argument('-w', '--wait', action='store_true', help="Wait for your vm to do whatever. Default true for applicable operations.")
        parser.add_argument('-f', '--force', action='store_true', help="Don't wait for vm's to be done doing things. Overrides -w.")
        parser.add_argument('-v', '--verbose', action='store_true', help="Get verbose output.")
        parser.add_argument('-V', '--version', action='version', version='%(prog)s {version}'.format(version=__version__))

        arrgs = parser.parse_args()

        if arrgs.version:
            #then we shouldn't be here right now.
            exit(0)

        # input validations imported from utils/validations.py
        _validate_args(arrgs)
        _validate_command(ICANN(), action=arrgs.action, host=arrgs.host)

        # handle force/wait options
        if arrgs.force:
            wait = 'false'
        elif arrgs.wait:
            assert str(arrgs.wait.lower()) in ('true', 'false'), 'value for <-w|--wait> must be <[true]|false>'
            wait = str(arrgs.wait.lower())
        else:
            wait = 'true'

        # handle credential-type
        if arrgs.json_credentials:
            cred_dict = load_host_creds()
            creds = (cred_dict['tenant_id'], cred_dict['client_id'], cred_dict['secret'])
        # This reads in the credentials in a specific way using regex, & needs to be passed an ascii file-object.
        # eventually I'll change and explain that way, but for now you can follow the rabbit hole if your IDE is good.
        elif arrgs.json_infile_credentials:
            cred_dict = load_host_creds(alt_infile=arrgs.json_infile_credentials)
            creds = (cred_dict['tenant_id'], cred_dict['client_id'], cred_dict['secret'])
        elif arrgs.infile:
            creds = arrgs.infile
        # yep. happens later.
        else:
            print 'WARNING: Credentials have not been passed in.\n You will need to enter them by hand.\n\n'
            creds = None


        # This is mostly a sanity check.
        # `wait` should be a bool & `creds` can be a filepath (aka a string), tuple, or NoneType.
        # regardless, they should both be defined by now. If this assert statement pops-off, thar B issues.
        assert wait and (creds or creds is None), 'argument error.'

        action_input, host_input = arrgs.action, arrgs.host

        if arrgs.verbose:
            ##########################################################
            print 'CURRENT CONFIG STATE:'
            ICANN().print_state()
            INP = raw_input('')
            if INP.lower() in ('q', 'n', 'quit', 'exit', 'no', 'abort'):
                exit(1)
            else: del INP; pass
            ##########################################################

        # This is what it's all about right hurrrrr:
        function_to_use = ICANN()['action_mappings'][action_input]
        rg, real_hostname = ICANN()['host_mappings'][host_input]


        # aaaaaaaaand GO!
        if wait == 'false':
            function_to_use(creds, resource_group=rg, vm=real_hostname, wait=False)
        else:
            function_to_use(creds, resource_group=rg, vm=real_hostname)

    # improper usage. Congrats tho; shouldn't be possible.
    else: exit(1)

if __name__ == '__main__':
    main()
