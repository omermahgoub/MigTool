__author__ = 'OmerMahgoub'
#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.abspath("/Projects/OpenStackAdapter"))

import novaclient.v2.client as nvclient
from Logger import VMLogger
from operator import itemgetter
import Auth
import networks
import UserAssignments
import random
import AdapterDBOperations

class OpenStackAdapterVMInstance(object):
    _objLogs = VMLogger()

    """ VM Related Function Starts Here """

    def CreateVM(self, VmName, ImageName, flavorName, network_label, ProjectName):
        try:
            objAuth = Auth.OpenStackAdapterAuth()
            objNetworks = networks.OpenStackAdapterNetworks()
            novacreds = objAuth.get_credentials("nova",ProjectName)
            objnova = nvclient.Client(**novacreds)

            objDBOperations = AdapterDBOperations.AdapterDBOperations()

            # Create a network and one subnet
            print "Creating Private Network"
            network = objNetworks.create_private_network(network_label,ProjectName)
            print "Printing Network %s", network
            # print network['NetworkDetails']['network']['id']

            if network['Status'] == True:
                print "Creating Private Router"
                # Plug a router between our private network and an external network
                router = objNetworks.create_router("Router_Id_" + str(random.randrange(0, 8000, 3)), network_label, "net04_ext",ProjectName)

                image = objnova.images.find(name=ImageName)
                flavor = objnova.flavors.find(name=flavorName)
                network_details = objnova.networks.find(label=network_label)

                # Creating Instance
                print "Creating Instance"
                instance = objnova.servers.create(name=VmName, image=image,
                                               flavor=flavor, key_name=None, nics=[{'net-id': network_details.id}])

                message = {'Status': True, 'ServerId': instance.id}
                objDBOperations.Create_Order_Requests(EventId, 'Pending',instance.id)
                return message
            else:
                message = {'Status': False}
                return message

        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            errMsg = "Project Name: %s and Error is %s " % (ProjectName, message)
            self._objLogs.Logger("CreateVM", 'critical', errMsg)
            return message

    """ VM Related Function Ends Here """

    def ResizeInstance(self, ServerId, FlavorName, ProjectName):
        try:
            objAuth = Auth.OpenStackAdapterAuth()
            objNetworks = networks.OpenStackAdapterNetworks()
            novacreds = objAuth.get_credentials("nova",ProjectName)
            objnova = nvclient.Client(**novacreds)

            print "Creating Instance"
            instance = objnova.servers.resize(server = ServerId, flavor = FlavorName)

            message = {'Status': True, 'ServerId': instance.id}
            return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            errMsg = "Project Name: %s and Error is %s " % (ProjectName, message)
            self._objLogs.Logger("CreateVM", 'critical', errMsg)
            return message


    def VMQueue(self, VmName, ImageName, FlavorName, ProjectName, EventId):

        """Creating the Instance of the Logging Message"""
        objLogs = VMLogger()
        # End

        try:
            objUsers = UserAssignments.OpenStackAdapterUsers()
            """"Initialization of Connection """""
            self._objLogs.Logger("VMQueue", "info", "Create VM Started")

            print "VM Creation Process Initiated"

            # Create VM
            vmStatus = self.CreateVM(VmName, ImageName, FlavorName, "net_id_" + str(random.randrange(0, 4000, 3)), ProjectName)

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
                message = template.format(vmStatus['Type'], vmStatus['Message'], ProjectName)
                objLogs.Logger("VMQueue", "critical", message)
                return {'Status': 'Error'}
        except Exception, e:
            template = "An exception of type {0} occurred. Details are:\n{1!r}."
            message = template.format(type(e).__name__, e.args)
            objLogs.Logger("VMQueue", "critical", message)
            return {'Status': 'Error'}
