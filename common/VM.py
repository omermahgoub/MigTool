__author__ = 'OmerMahgoub'

#!/usr/bin/env python
import novaclien.client as nvclient
from Logger import VMLogger
from operator import itemgetter
from common.Auth import OpenStackAdapterAuth as OpenStackAuth
from networks import OpenStackAdapterNetworks
from UserAssignments import OpenStackAdapterUsers
import random
import AdapterDBOperations

class OpenStackAdapterVMInstance(object):
    _objLogs = VMLogger()

    """ VM Related Function Starts Here """
    #CreateVM(CustomerName, UserName, VmName, ImageName, FlavorName, "net_id_" + str(random.randrange(0, 4000, 3)), EventId)
    def CreateVM(self, CustomerName, UserName, VmName, ImageName, flavorName, network_label, EventId, TenantId):
        try:
            objAuth = OpenStackAuth()
            objNetworks = OpenStackAdapterNetworks()
            novacreds = objAuth.get_nova_neutron_credentials("nova", UserName, CustomerName)
            objnova = nvclient.Client(**novacreds)

            objDBOperations = AdapterDBOperations.AdapterDBOperations()

            # Create a network and one subnet
            print "Creating Private Network"
            network = objNetworks.create_private_network(UserName, CustomerName, network_label)
            print "Printing Network %s", network
            # print network['NetworkDetails']['network']['id']

            if network['Status'] == True:
                print "Creating Private Router"
                # Plug a router between our private network and an external network
                #(self, name, private_net_name, public_net_name, UserName, CustomerName):
                #("Router_7865","net_id_7865","net04_ext",'mamerpasha','MiracleSoft1')
                router = objNetworks.create_router("Router_Id_" + str(random.randrange(0, 8000, 3)), network_label, "net04_ext", UserName, CustomerName)

                print "Router Information %s" % router

                image = objnova.images.find(name=ImageName)
                flavor = objnova.flavors.find(name=flavorName)
                network_details = objnova.networks.find(label=network_label)

                print "Tenant ID from Queue %s" % TenantId

                securityRule = objNetworks.create_security_rules(UserName, CustomerName, TenantId)
                print "Security Rule %s" % securityRule

                print "Creating Instance"
                print "Image %s" % image
                print "ImageName Parameter %s" % ImageName
                print "FlavorName from Parameter %s" % flavorName
                print "Flavor Name %s" % flavor
                print "VM Name %s" % VmName
                print "Key Name %s" % UserName+"_key"
                print "Network ID %s" % network_details.id

                # Creating Instance
                print "Creating Instance"
                # instance = objnova.servers.create(name=VmName, image=image,
                #                                flavor=flavor, key_name=UserName+"_key", nics=[{'net-id': network_details.id}])
                instance = objnova.servers.create(name=VmName, image=image,
                                               flavor=flavor, key_name=None, nics=[{'net-id': network_details.id}])

                message = {'Status': True, 'ServerId': instance.id}
                #objDBOperations.Create_Order_Requests(EventId, 'InProgress',instance.id)

                return message
            else:
                message = {'Status': False}
                return message

        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': str(e)}
            errMsg = "Customer Name: %s and Error is %s " % (CustomerName, message)
            self._objLogs.Logger("CreateVM", 'critical', errMsg)
            print message
            self._objLogs.Logger("VM Creation Failed",'critical',message)
            return message

    """ VM Related Function Ends Here """

    def ResizeInstance(self, ServerId, FlavorName, ProjectName):
        try:
            objAuth = OpenStackAuth()
            objNetworks = OpenStackAdapterNetworks()
            novacreds = objAuth.get_credentials("nova",ProjectName)
            objnova = nvclient.Client(**novacreds)

            print "Creating Instance"
            instance = objnova.servers.resize(server = ServerId, flavor = FlavorName)

            message = {'Status': True, 'ServerId': instance.id}
            return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': str(e)}
            errMsg = "Project Name: %s and Error is %s " % (ProjectName, message)
            self._objLogs.Logger("CreateVM", 'critical', errMsg)
            return message

    #CustomerName, UserName, "VM_" + str(random.randrange(0, 10, 1)), imageName, flavorname, EventId, tenantId
    def VMQueue(self, CustomerName, UserName, VmName, ImageName, FlavorName, EventId, TenantId):

        """Creating the Instance of the Logging Message"""
        objLogs = VMLogger()
        # End

        try:
            objUsers = OpenStackAdapterUsers()
            """"Initialization of Connection """""
            self._objLogs.Logger("VMQueue", "info", "Create VM Started")

            print "VM Creation Process Initiated"

            # Create VM
            vmStatus = self.CreateVM(CustomerName, UserName, VmName, ImageName, FlavorName, "net_id_" + str(random.randrange(0, 4000, 3)), EventId, TenantId)

            objLogs.Logger("VMQueue", "info", "VM Process Completed")

            if vmStatus['Status'] not in ('Error',False):
                if vmStatus['Status'] == True:

                    """ Now we will disassociate SuperAdmin with the Project """

                    #userDisassociateStatus = objUsers.DisassociateUserFromProject(ProjectName)

                    """ End of Disassoication of SuperUser with the Project """
                    message = {'Status': True}
                else:
                    message = {'Status': False}
                return message
            else:
                template = "An exception of type {0} occurred. Details are:\n{1!r}. Parameters are:\n{2!r}"
                message = template.format(vmStatus['Type'], vmStatus['Message'], CustomerName)
                objLogs.Logger("VMQueue", "critical", message)
                return {'Status': 'Error'}
        except Exception, e:
            template = "An exception of type {0} occurred. Details are:\n{1!r}."
            message = template.format(type(e).__name__, str(e))
            objLogs.Logger("VMQueue", "critical", message)
            return {'Status': 'Error'}