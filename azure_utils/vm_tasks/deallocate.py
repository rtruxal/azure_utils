import re
from os.path import exists
from azure_utils.core.get_azure_clients import get_service_principal_token, produce_clients
from azure_utils.utils.log_funcs import INFO_expected_exception, WARN_unexpected_exception


@WARN_unexpected_exception
def _parse_specs(infile):
    # If we're using JSON the creds will be a tuple at this point. Not an infile.
    # so let's just call the tuple credential option inside of this aptly named function.
    if isinstance(infile, tuple) and len(infile) == 3:
        return infile
    if not exists(infile):
        raise IOError()
    regex = r':\s+(.*)$'
    with open(infile, 'rb+') as secrets:
        messy_isht = secrets.read()
    return re.findall(regex, messy_isht, flags=re.MULTILINE)

@INFO_expected_exception
def deallocate(infile, resource_group=None, vm=None, wait=True, return_client=False):
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
    # import pdb
    # pdb.set_trace()
    street_creds = get_service_principal_token(appid=appid, secret=secret, tenantid=tenantid)
    compute_client = produce_clients(street_creds)
    if wait:
        compute_client.virtual_machines.deallocate(resource_group, vm).wait()
    else:
        compute_client.virtual_machines.deallocate(resource_group, vm)
        print 'WARN: deallocate-machine was called & success/failure indicator was bypassed!'
    if return_client:
        return compute_client
    else:
        return 0
