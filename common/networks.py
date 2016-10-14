__author__ = 'OmerMahgoub'

#!/usr/bin/env python
import keystoneclient.v2_0.client as ksclient
import novaclient.v2.client as nvclient
import neutronclient.v2_0.client as neclient
from Logger import VMLogger
from operator import itemgetter
from common.Auth import OpenStackAdapterAuth as OpenStackAuth

class OpenStackAdapterNetworks(object):
    _objLogs = VMLogger()
    

    """ Network Related Stuff Starts Here """
    #UserName, CustomerName, network_label
    def create_private_network(self,UserName, CustomerName, network_name):
        """Create a private network and subnets. To remain readable this function
        won't do any error checking.

        :param network_name: the name of the private network
        :param cidr_list: an iterable of subnet cidr notations
        """
        objAuth = OpenStackAuth()
        try:
            credentials =  objAuth.get_nova_neutron_credentials("neutron", UserName, CustomerName)

            neutron = neclient.Client(**credentials)

            body_sample = {'network': {'name': network_name,
            'admin_state_up': True}}

            netw = neutron.create_network(body=body_sample)
            net_dict = netw['network']
            network_id = net_dict['id']

            # We may want to create several subnets in this network
            # for cidr in cidr_list:
            #     body_create_subnet = {'subnets': [{'cidr': cidr,
            #                                        'ip_version': 4,
            #                                        'network_id': network_id}]}

            # body_create_subnet = {'name':network_name +'_sub',
            # 'subnets': [{'cidr': '10.0.0.0/24',
            # 'ip_version': 4, 'network_id': network_id}]}

            body_create_subnet = {'subnets': [{'cidr': '10.0.0.0/24',
                                               'ip_version': 4,
                                               'network_id': network_id,
                                               'name':network_name +'_sub'}]}

            subnet = neutron.create_subnet(body=body_create_subnet)

            message = {'Status':True,'NetworkDetails': netw}
            return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': str(e)}
            errMsg = "Project Name: %s and Error is %s " % (network_name, message)
            self._objLogs.Logger("create_private_network", 'critical', errMsg)
            return message
    #("Router_Id_" + str(random.randrange(0, 8000, 3)), network_label, "net04_ext", UserName, CustomerName)
    def create_router(self, name, private_net_name, public_net_name, UserName, CustomerName):
        """Creates a NAT router that will allow VMs on the private net to
        connect to the internet through the public net.

        :param name: Name the router.
        :param private_net_name: Name of the private network where our VMs
                                 will be spawned.
        :param public_net_name: Name of the public network connected to
                                the internet.
        """
        objAuth = OpenStackAuth()
        try:
            credentials =  objAuth.get_nova_neutron_credentials("neutron", UserName, CustomerName)
            neutron = neclient.Client(**credentials)

            prv_subnet_id = neutron.list_networks(
                name=private_net_name)['networks'][0]['subnets'][0]
            pub_net_id = neutron.list_networks(
                name=public_net_name)['networks'][0]['id']

            req = {
                "router": {
                    "name": name,
                    "external_gateway_info": {
                        "network_id": pub_net_id
                    },
                "admin_state_up": True
                }
            }
            router = neutron.create_router(body=req)
            router_id = router['router']['id']

            req = {
                "subnet_id": prv_subnet_id
            }
            neutron.add_interface_router(router=router_id, body=req)

            message = {'Status':True,'RouterDetails': router}
            return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': str(e)}
            errMsg = "Project Name: %s and Error is %s " % (name, message)
            self._objLogs.Logger("create_router", 'critical', errMsg)
            return message

    def create_security_rules(self, UserName, CustomerName, TenantId):
        """Creates a NAT router that will allow VMs on the private net to
        connect to the internet through the public net.

        :param name: Name the router.
        :param private_net_name: Name of the private network where our VMs
                                 will be spawned.
        :param public_net_name: Name of the public network connected to
                                the internet.
        """
        objAuth = OpenStackAuth()
        try:
            credentials =  objAuth.get_nova_neutron_credentials("neutron", UserName, CustomerName)
            neutron = neclient.Client(**credentials)


            list_groups = neutron.list_security_groups()

            security_group_id = ""

            for groups in list_groups.iterkeys():
                groupvalues = list_groups[groups]
                for lstGroup in groupvalues:
                    if lstGroup['name'] == 'default':
                        security_group_id = lstGroup['id']

            RuleData  = {'security_group_rules':[{'remote_group_id': None,'direction': 'egress','remote_ip_prefix': '0.0.0.0/0','protocol': 'tcp',
                                                  'tenant_id': TenantId,'port_range_max': 80,
                                                  'security_group_id': security_group_id,'port_range_min': 80,'ethertype': 'IPv4'}]}
            print neutron.create_security_group_rule(body=RuleData)

            message = {'Status':True}
            return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': str(e)}
            errMsg = "Project Name: %s and Error is %s " % (UserName, message)
            self._objLogs.Logger("create_security_rules", 'critical', errMsg)
            return message

    """ Network Related Stuff Ends Here """
#
#
# objTest = OpenStackAdapterNetworks()
#
# print objTest.create_private_network('mamerpasha','MiracleSoft1','net_id_7865')
# print objTest.create_router("Router_7865","net_id_7865","net04_ext",'mamerpasha','MiracleSoft1')