from msrestazure.azure_active_directory import ServicePrincipalCredentials as SPC
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient

from azure_utils.utils.custom_errors import ArgumentException
from azure_utils.utils.json_ingress import load_sub_id


# yaaaaaay The Class!!
class ClientFactory(object):

    # Get the sub-id from your json data file.
    # THIS IS NOT OPTIONAL.
    AZURE_SUB_ID = load_sub_id()
    # THIS IS NOT OPTIONAL.

    ###
    # Static Functions for use only within the class
    ###
    @staticmethod
    def _convert_to_int(value):
        try:
            return int(value)
        except Exception:
            print '{} could not be converted to an int'.format(value)
            return 0

    @classmethod
    def _gen_resource_clients(cls, int_quantity, credential_token):
        assert type(int_quantity) is int and int_quantity > 0
        return [ResourceManagementClient(credential_token, cls.AZURE_SUB_ID) for i in range(int_quantity)]

    @classmethod
    def _gen_network_clients(cls, int_quantity, credential_token):
        assert type(int_quantity) is int and int_quantity > 0
        return [NetworkManagementClient(credential_token, cls.AZURE_SUB_ID) for i in range(int_quantity)]

    @classmethod
    def _gen_compute_clients(cls, int_quantity, credential_token):
        assert type(int_quantity) is int and int_quantity > 0
        return [ComputeManagementClient(credential_token, cls.AZURE_SUB_ID) for i in range(int_quantity)]

    ###
    # a bunch of work for single class-attr, the client-list.
    ###
    def __init__(self, resource=0, network=0, compute=0, credentials=None):
        """
        Each param value specifies the number of clients you want of that type.
        All the params below need to be either ints, or easily convertable to ints.

        credentials must be either type:
         - azure.common.credentials.ServicePrincipalCredentials()
            - If only one SPC is passed, all clients will use it.
        OR
         - a json-like mapping thereof.
            - FORMAT:
                {'[resource|network|compute]' : (credential_token, quantity_of_clients)}

        :param resource: 
        :param network: 
        :param compute: 
        :param credentials: (TODO: MAKE THIS WORK for dicts) type == json or dict. 
        
        :var self.clients: is a list of the clients that'cha just made. Access via just using __repr__ 
             or as a generator using `get_client_generator()'

        """
        assert isinstance(credentials, ServicePrincipalCredentials) or isinstance(credentials, SPC)
        if not resource and not network and not compute:
            raise ArgumentException('Must specify a client-type')

        clients = []
        resource_nums, network_nums, compute_nums = [self._convert_to_int(i) for i in (resource, network, compute)]

        if resource_nums:
            clients.append(self._gen_resource_clients(resource_nums, credentials))
        if network_nums:
            clients.append(self._gen_network_clients(network_nums, credentials))
        if compute_nums:
            clients.append(self._gen_compute_clients(compute_nums, credentials))

        self.clients = clients
    ###
    # little pointless that both do the same thing but meh.
    ###
    def __repr__(self):
        return self.clients

    def get_client_generator(self):
        for client in self.clients:
            yield client
