from azure_utils.utils.custom_errors import JSONInfileConfigException, FeatureNotYetImplemented
from azure_utils.utils.json_ingress import load_host_config
from azure_utils.utils.log_funcs import INFO_expected_exception

class NamesBase(dict):
    def __init__(self):
        from azure_utils.vm_tasks import turn_on, turn_off, deallocate, status_of
        super(NamesBase, self).__init__()
        # supported actions to take on VMs
        self['actions'] = (
            'turnon',
            'turnoff',
            'deallocate',
            'statusof'
        )

        # action mappings
        self['action_mappings'] = {
            'turnon': turn_on.boot,
            'turnoff': turn_off.shut_down,
            'deallocate': deallocate.deallocate,
            'statusof': status_of.status,
        }

# This name was chosen in favor of brevity.
# Basically a dictionary.
class ICANN(NamesBase):
    """
    ICANN is the place where all the important names & numbers are stored.
    Much like ICANN, this class is a shitty swiss-army-knife of all runtime host info.
    """
    def __init__(self, use_json_config=True, alt_config_file=None):
        super(ICANN, self).__init__()
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


    def return_state(self):
        foo_bucket = []
        for attribute in [k for k, v in self.__dict__ if v]:
             foo_bucket.append('{}:  {}\n'.format(attribute, self.__dict__[attribute]))
        return '\n'.join(foo_bucket)

    # Hopefully this overrides stuff.
    def __setattr__(self, key=None, value=None):
        pass

class StatusTracker(NamesBase):
    def __init__(self, use_json_config=True, alt_config_file=None):
        super(StatusTracker, self).__init__()
        if use_json_config is True:
            self.update(load_host_config(alt_infile=alt_config_file))
        else:
            raise FeatureNotYetImplemented('as of now, the -a option only supports utilizing a JSON config file.')
        self['statuses'] = dict()
        self.status_func = self['action_mappings']['statusof']

    @INFO_expected_exception
    def get_all_vm_statuses(self, creds, simple=True):
        for hostdict in self['hosts']:
            if simple is False:
                print hostdict['cmdline_hostname'].upper() + ':'
            try:
                # Jesus fucking christ...
                self['statuses'].update((hostdict['cmdline_hostname'],
                                         self.status_func(creds, vm=hostdict['azure_hostname'],
                                                          resource_group=hostdict['resource_group'], simple=simple)))
            except Exception:
                pass
            if simple is False:
                print '\n'

    def print_state(self):
        print self['statuses']