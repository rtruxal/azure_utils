import sys
import argparse
from azure.common.credentials import ServicePrincipalCredentials
from .client_factory import ClientFactory # <--Mine

__doc__ = """
------------------------------------------------------------------------------------------------------------------------
     WELCOME TO THE INTERFACE MODULE FOR THE 
             AZURE CLIENT FACTORY!

         You're gonna love it. Promise. 

       =====================================
                SHORT DESCRIPTION:
       =====================================

This module creates a credential token from your input & uses
a client-factory class to make "Client" objects of various types.

Azure "Client" objects require authentication to instantiate. consequently: 
good luck using the client_factory module without this interface-module.

       =====================================
              LESS-SHORT DESCRIPTION:
       =====================================

This entire package assumes you have created a
            "Service Principal"
from within your Azure ActiveDirectory settings.

Creating a "Service Principal" essentially asks AAD:
 - "Hey! I made an app that's gonna mess with my 
    subscription. Please allow it to do stuff."

Azure Active Directory will respond with:
 - "Ok cool, here are 3 important numbers that
    your app is gonna need when it tries to connect."

At this point, you should stop talking to the computer. 
Waht are you crazy?   

       =====================================
            WAHT 3 IMPORTANT NUMBERS????
       =====================================

The following 3 arguments belong to the magical function 
          "get_service_principal_token()"
They also happen to be the "...3 important numbers..." that AAD was talking about during your 
aforementioned little dialogue with your computer-screen.

get_service_principal_token():
    :param appid: your app-id (aka client-ID)
    :param secret: you got a secret when you registered your app. If you don't remember it you'll need a new one.
    :param tenantid: this is the "subscription" id for your app's AzureActiveDirectory "subscription."
                     See link above for clarification. (I don't make the rules, I just attempt to follow them)

fin.

------------------------------------------------------------------------------------------------------------------------

#CURRENT FUNCTIONALITY


As of the time of creation, 3 types of clients can be created with this interface:
 - resource-management clients (keyword: 'resource')
 - network-management clients (keyword: 'network')
 - compute-management clients (keyword: 'compute')

------------------------------------------------------------------------------------------------------------------------

#DEVELOPING & CONTRIBUTING


If you would like to allow for more types of clients, please make additions in the following locations:
 - within the ClientFactory class inside of the .client_factory module in this directory.
 - in the `produce_clients()` function below, change the variable `possible_client_types` to include your keyword.
    - KEEP IN MIND: your dictionary mapping for `alt_clientfactory_param_dict` must match the keyword you use above.

------------------------------------------------------------------------------------------------------------------------
"""




def get_service_principal_token(appid, secret, tenantid):

    """
    -------------------------------------

    Make a Service Principal authentication token and return it.
    
    See the following link for a walkthrough:
        - https://azure.microsoft.com/en-us/documentation/articles/resource-group-create-service-principal-portal/

    :param appid: your app-id (aka client-ID)
    :param secret: you got a secret when you registered your app. If you don't remember it you'll need a new one.
    :param tenantid: this is the "subscription" id for your app's AzureActiveDirectory "subscription."
                     See link above for clarification. (I don't make the rules, I just attempt to follow them)

    -------------------------------------
    Important note:
    !DON'T MESS WITH THIS UNLESS YOU WANT TO DELVE HEADFIRST INTO AzureActiveDirectory-HELL.!
    -------------------------------------
    -------------------------------------
    """
    credentials = ServicePrincipalCredentials(
        client_id=appid,
        secret=secret,
        tenant=tenantid
    )
    return credentials


def produce_clients(credential_token, alt_clientfactory_param_dict=None):
    """
    -------------------------------------

    :param credential_token:
        This is obtained from the function `get_service_principal_token(*args)`
        which can be found within this module.

    -------------------------------------

    :param alt_clientfactory_param_dict:
        FORMAT:
                {
                  'resource' : <positive_int_or_0>,
                  'network'  : <positive_int_or_0>,
                  'compute' : <positive_int_or_0>,
                }
    :return: A list of authenticated client-objects.

    -------------------------------------
    """
    ## default behavior spits back a compute client for messing w/ existing VMs.
    possible_client_types = ('resource', 'network', 'compute')
    if not alt_clientfactory_param_dict:
        client = ClientFactory(compute=1, credentials=credential_token).__repr__()
        return client[0][0]

    # see docstring above to use this.
    else:
        # I should probably use namedtuples, but dictionaries are easy.
        assert isinstance(alt_clientfactory_param_dict, dict)
        for k, v in alt_clientfactory_param_dict.items():
            assert k in possible_client_types, \
                "invalid key: {} \nin clientfactory param-dict passed to constructor".format(k)
            assert type(v) is int, \
                "invalid value: {}\nin clientfactory param-dict passed to constructor".format(v)

        # regularize dict
        for entry in possible_client_types:
            if entry not in alt_clientfactory_param_dict:
                alt_clientfactory_param_dict[entry] = 0
            else: pass
        assert len(alt_clientfactory_param_dict.keys()) == len(possible_client_types)
        # make'a-de-clients!
        clients = ClientFactory(
            resource=alt_clientfactory_param_dict['resource'],
            network=alt_clientfactory_param_dict['network'],
            compute=alt_clientfactory_param_dict['compute'],
            credentials=credential_token
        )
        return clients

def get_resource_client(credential_token):
    return produce_clients(credential_token=credential_token, alt_clientfactory_param_dict={'resource' : 1})

def get_compute_client(credential_token):
    return produce_clients(credential_token=credential_token)

def get_network_client(credential_token):
    return produce_clients(credential_token=credential_token, alt_clientfactory_param_dict={'network' : 1})


def main(appid, secret, tenantid):
    "instantiates authenticated clients for each supported type & prints docstring"
    # credentialize
    street_creds = get_service_principal_token(appid=appid, secret=secret, tenantid=tenantid)
    # clientize
    resource_client = get_resource_client(street_creds)
    compute_client = get_compute_client(street_creds)
    network_client = get_network_client(street_creds)
    # printitize
    print resource_client.__doc__
    print compute_client.__doc__
    print network_client.__doc__

if __name__ == '__main__':
    #TODO: MAKE THIS USEFUL IN ANY WAY SHAPE OR FORM.
    #      - For example: returning python client objects to stdout is dumb and won't work.
    #      - Currently all argparse is doing is checking to see if your creds have proper format.
    #      - It also prints documentation on the client objects you are (hopefully) able to instantiate.

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--appid', help='App id, (aka Client id.) Ex: aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee')
    parser.add_argument('-s', '--secret', help='secret-codes n\' there is a file. u gotta know this to play.')
    parser.add_argument('-t', '--tenantid', help='Tenant id. Ex: aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee')
    args = parser.parse_args()

    #PREACH!
    sys.stderr.write('\n!!!!\n\nTHIS MODULE IS NOT READY TO BE RUN FROM THE COMMAND LINE.\n\n!!!!\n')

    appid = args.appid
    secret = args.secret
    tenantid = args.tenantid

    if not appid:
        appid = raw_input('Enter app ID (client ID):')
    if not secret:
        secret = raw_input('Enter secret:')
    if not tenantid:
        tenantid = raw_input('Enter the Azure Active Directory tenant-ID for this app:')
    # aaaaaand go!
    main(appid=appid, secret=secret, tenantid=tenantid)

#######################################################################################
## This is an interesting `sys` method that shits strings to stdout.
## Not sure about benefits over `print foo` which appears to do the same thing...
##------------------------------------------------------------------------------------
#sys.stdout.write(get_compute_client(appid=appid, secret=secret, tenantid=tenantid))
##------------------------------------------------------------------------------------
#######################################################################################