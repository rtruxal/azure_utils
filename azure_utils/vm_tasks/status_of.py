import re
from os.path import exists
from azure_utils.core.get_azure_clients import get_service_principal_token, produce_clients
from azure_utils.utils.log_funcs import INFO_expected_exception, WARN_unexpected_exception


@WARN_unexpected_exception
def _parse_specs(infile):
    # Let's just include the tuple one inside of this function.
    if isinstance(infile, tuple) and len(infile) == 3:
        return infile
    if not exists(infile):
        raise IOError()
    regex = r':\s+(.*)$'
    with open(infile, 'rb+') as secrets:
        messy_isht = secrets.read()
    return re.findall(regex, messy_isht, flags=re.MULTILINE)


def get_single_vm_status(vm_instance, simple=True):
    if not vm_instance.instance_view:
        raise AssertionError('the vm-object passed to this function must have been created to show its instance-view.')

    hostname = vm_instance.name
    if simple:
        def __decision_tree_for_simplified_output(vm_name, instance_view_statuses_list):
            assert len(instance_view_statuses_list) is 2
            # shorthand
            ivsl = instance_view_statuses_list
            if u'updating' in ivsl[0].display_status.lower():
                return '{} is currently updating.'.format(vm_name)
            elif u'running' in ivsl[1].display_status.lower():
                return '{} is currently running. Machine time: {}'.format(vm_name, ivsl[0].time)
            elif u'stopped' in ivsl[1].display_status.lower():
                return '{} is currently stopped (vm is still allocated).'.format(vm_name)
            elif u'deallocated' in ivsl[1].display_status.lower():
                return '{} is currently deallocated. Last machine time: {}'.format(vm_name, ivsl[0].time)
            else:
                return '_UNKNOWN_'
        response = __decision_tree_for_simplified_output(vm_name=hostname, instance_view_statuses_list=vm_instance.instance_view.statuses)
        if response == '_UNKNOWN_':
            # Then shit dawg. I clearly didn't think of every case or the rules in __dtfso() aren't bulletproof.
            # The thing below is prly not gonna work but let's try it anyway.
            pass
        else:
            # NOTICE THE RETURN STATEMENT HERE.
            return {'current_status' : response}

    #TODO: POTENTIALLY MAKE THESE LESS DEPENDANT ON THE SPECIFIC STRUCTURE OF OBJECT-LINKS.
    answerdict = dict()
    answerdict['location'] = vm_instance.location
    answerdict['resource_id'] = vm_instance.vm_id
    answerdict['prov_state'] = vm_instance.instance_view.statuses[0].display_status
    answerdict['last_up'] = vm_instance.instance_view.statuses[0].time
    answerdict['power_state'] = vm_instance.instance_view.statuses[1].display_status
    answerdict['hostname'] = hostname
    return answerdict


@INFO_expected_exception
def status(infile, resource_group=None, vm=None, wait=True, return_client=False, return_vm=False, simple=True):
    if not resource_group or not vm:
        raise AssertionError('you must specify both a vm and a resource_group')
    try:
        tenantid, appid, secret = _parse_specs(infile)
        tenantid = tenantid.strip('\r')
        appid = appid.strip('\r')
        secret = secret.strip('\r')
    except IOError or TypeError:
        try:
            tenantid, appid, secret = infile
        except Exception:
            print 'Enter credentials manually (or press Ctrl + C to abort):'
            tenantid = raw_input('enter the exact tenant ID including dashes.')
            appid = raw_input('enter the exact Application/Client ID including dashes.')
            secret = raw_input('enter your secret service-principal code.')

    street_creds = get_service_principal_token(appid=appid, secret=secret, tenantid=tenantid)

    compute_client = produce_clients(street_creds)

    if wait:
        # garbagio, but need to keep for consistency.
        pass

    # DONT UNCOMMENT THESE. IT CREATES A CIRCULAR REF WHICH IS DUMB BUT WHATEVER.
    # TODO: put all validations in the "validations.py" file. That's what it's made for dude.
    # from azure.mgmt.compute import ComputeManagementClient
    # assert isinstance(compute_client, ComputeManagementClient)
    vm_instance = compute_client.virtual_machines.get(resource_group, vm, expand='instanceview')
    vm_status_dict = get_single_vm_status(vm_instance=vm_instance, simple=simple)

    # `simple=True` *should* be the only case wherein there is only 1 item in `vm_status_dict`.
    if len(vm_status_dict.values()) == 1:
        status_output_text = vm_status_dict.values()[0]
    else:
        #TODO: This is def not the best way to do this.
        status_output_list = []
        for k, v in vm_status_dict.items():
            status_output_list.append('{}: ==> {}'.format(k, v))
        status_output_text = '\n'.join(status_output_list)

    if return_client and return_vm:
        raise AssertionError('You cannot get back both a VM instance & its originating client. \
        \nConsequently only one of these can be set to True.')
    elif return_client:
        try:
            print status_output_text
        except Exception:
            pass
        finally:
            return compute_client
    elif return_vm:
        try:
            print status_output_text
        except Exception:
            pass
        finally:
            return vm_instance
    else:
        try:
            print status_output_text
        except Exception:
            print 'cannot print status at this time.'
        finally:
            return status_output_text