#!/usr/bin/env python

import argparse

from _version import __version__
from azure_utils.core.StateMachines import ICANN, StatusTracker
from azure_utils.utils.log_funcs import WARN_unexpected_exception
from azure_utils.utils.json_ingress import load_host_creds
from azure_utils.utils.validations import _validate_args, _validate_command


def main(args=None):
    if args is None:
        #TODO: Make an abstract & unified `Interface` class to handle these args.
        parser = argparse.ArgumentParser()
        parser.add_argument('action', nargs="?", help='options are <turnon|turnoff|deallocate|statusof>')
        parser.add_argument('host', nargs="?", help='select a host using `cmdline_hostname` from azure_utils/data/config/host_config.json <foo_host_1|foo_host_2|etc...>')
        parser.add_argument('-j', '--json-credentials', action='store_true', default=False, help="use the internal PLAINTEXT data file, 'credentials_config.json', for Azure credentials. Default is False 'cuz this is dangerous if you don't read & follow the WARNING.txt file.")
        parser.add_argument('-J', '--json-infile-credentials', nargs="?", type=argparse.FileType('r'), default=None, help="pass in a JSON file-path containing your credentials. See credentials_config.json for format.")
        parser.add_argument('-i', '--infile-credentials', nargs="?", type=argparse.FileType('r'), default=None, help="pass in a text file-path containing your credentials. See example_credfile.txt for format.")
        parser.add_argument('-w', '--wait', action='store_true', help="Wait for your vm to do whatever. Default true for applicable operations.")
        parser.add_argument('-f', '--force', action='store_true', help="Don't wait for vm's to be done doing things. Overrides -w.")
        parser.add_argument('-v', '--verbose', action='store_true', help="Get verbose output.")
        parser.add_argument('-V', '--version', action='version', version='%(prog)s {version}'.format(version=__version__), default=None)
        parser.add_argument('-a', '--all', action='store_true', default=False, help='perform specified action on all hosts.')
        parser.add_argument('-l', '--longform', action='store_true', default=False, help='Used in conjunction with `statusof` to give more detailed reports on each host.')
        arrgs = parser.parse_args()

        if arrgs.version:
            #then we shouldn't be here right now.
            exit(0)

        # if an action isn't specified let's pretend we wanna just see status
        if not arrgs.action:
            @WARN_unexpected_exception
            def __this_function_exists_so_i_can_log_things_using_a_decorator(arrgs):
                print 'WARNING: An action was not specified. Assuming the idempotent `statusof`.\n'
                return 'statusof'
            arrgs.action = __this_function_exists_so_i_can_log_things_using_a_decorator(arrgs=arrgs)

        # input validations imported from utils/validations.py
        _validate_args(arrgs)
        _validate_command(ICANN(), action=arrgs.action, host=arrgs.host, all=arrgs.all)

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


        # The following assert statement is mostly a sanity check...
        # `wait` should be a bool-in-a-string. Assert works since `bool('false') == True`
        # `creds` can be a filepath (aka a string), tuple, or NoneType.
        # regardless, they should both be defined by now. If this assert statement pops-off, thar B issues.
        assert wait and (creds or creds is None), 'argument error.'

        # NOW BEGINS THE DECISION TREE.
        #TODO: BUILD THE FOLLOWING LOGIC INTO AN `Interface` OBJECT THAT SUBCLASSES `ABCMeta` FROM THE `abc` MODULE.
        InMemoryDataStore = ICANN()
        action_input, host_input, operate_on_all, longform = arrgs.action, arrgs.host, arrgs.all, arrgs.longform
        # This is what it's all about right hurrrrr:
        function_to_use = InMemoryDataStore['action_mappings'][action_input]

        if arrgs.verbose:
            ##########################################################
            print 'CURRENT CONFIG STATE:'
            icann_state = InMemoryDataStore.return_state()
            if not icann_state:
                print 'Current state-config unavailable or empty.'
            else:
                print icann_state
            INP = raw_input('Continue? (y/n): ')
            if INP.lower() in ('q', 'n', 'quit', 'exit', 'no', 'abort'):
                exit(1)
            else: del INP; pass
            ##########################################################

        # aaaaaaaaand GO!
        if operate_on_all:
            if longform:
                return_val = StatusTracker().get_all_vm_statuses(creds=creds, simple=False)
            else:
                return_val = StatusTracker().get_all_vm_statuses(creds=creds)
            if return_val:
                return return_val
            else: exit(0)
        else:
            rg, real_hostname = InMemoryDataStore['host_mappings'][host_input]

            if wait == 'false':
                return_val = function_to_use(creds, resource_group=rg, vm=real_hostname, wait=False)
            else:
                return_val = function_to_use(creds, resource_group=rg, vm=real_hostname)

            if return_val:
                return return_val
    # improper usage.
    # Congrats tho; shouldn't be possible.
    else: exit(1)

if __name__ == '__main__':
    main()
