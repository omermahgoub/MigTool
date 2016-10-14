#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.abspath("/Projects/OpenStackAdapter"))

import novaclient.v2.client as nvclient
from Logger import VMLogger

import Auth

class OpenStackAdapterVMStatus(object):
    _objLogs = VMLogger()

    def GetServerStatus(self, UserName, CustomerName, ServerId):
        try:
            objAuth = Auth.OpenStackAdapterAuth()
            novacreds = objAuth.get_nova_neutron_credentials("nova", UserName, CustomerName)
            objnova = nvclient.Client(**novacreds)

            print UserName
            print CustomerName



            servers_status = objnova.servers.get(ServerId)
            message = {'Status': True,'ServerStatus':servers_status.status}
            return message

        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            return message

#objTest = OpenStackAdapterVMStatus()
#print objTest.GetServerStatus('turki89','Turki_45','f1ea08f5-9bef-4337-a8a0-d4c217619095')
