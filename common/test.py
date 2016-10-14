#!/usr/bin/env python
import novaclient.v2.client as nvclient
import keystoneclient.v2_0.client as ksclient

class OpenStackAdapterProjects(object):
    def get_credentials(service,projectname):
        """Returns a creds dictionary filled with the following keys:

        * username
        * password (depending on the service)
        * project_id (depending on the service)
        * auth_url

        :param service: a string indicating the name of the service
                        requesting the credentials.
        """
        if service.lower() in ("keystone", "neutron"):
            creds = {'auth_url': '', 'username': '', 'password': '', 'tenant_name': ''};
            creds['auth_url'] = "http://172.18.101.3:5000/v2.0"
            creds['username'] = "aoulah"
            creds['password'] = "12345678"
            creds['tenant_name'] = "admin"
            return creds
        elif service.lower() in ("nova", "cinder"):
            creds = {'username': '', 'api_key': '', 'auth_url': '', 'project_id': ''};
            creds['username'] = "aoulah"
            creds['api_key'] = "12345678"
            creds['auth_url'] = "http://172.18.101.3:5000/v2.0"
            creds['project_id'] = projectname
            # creds['service_type'] = "admin"
            return creds
#
    kcreds = get_credentials("keystone", "admin")
    ncreds = get_credentials("nova", "admin")

    _objkeystone = ksclient.Client(**kcreds)
    _objnova = nvclient.Client(**ncreds)



    def Project_Availability(self, ProjectName):
        """
        :param ProjectName: a string indicating the name of the Project
                        requesting the Project Availability.
        """
        tenantId = ""
        tenant_lists = self._objkeystone.tenants.list()
        print tenant_lists

        for tenant in tenant_lists:
            if tenant.name == ProjectName:
                tenantId = tenant.id
        # print self._objkeystone.auth_token
        #
        # print self._objnova.servers.list()
        # print self._objkeystone.tenants.list_users("22e4dba9d25e408f852264629252abe2")
        #
        print self._objnova.servers.list()

        if tenantId == "":
            message = {'Status': False}
            return message
        else:
            message = {'Status': True}
            return message
        # except Exception, e:
        #     message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
        #     return message

    def CreateProject(self, ProjectName):
        try:
            print self._objkeystone.tenants.create(ProjectName, description=None, enabled=True)
            message = {'Status': True}
            return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            errMsg = "Tenant Name: %s and Error is %s " % (ProjectName, message)
            self._objLogs.Logger("CreateProject", 'critical', errMsg)
            return message


objTest = OpenStackAdapterProjects()
print objTest.Project_Availability("admin")
print objTest.CreateProject("Zubi Bhai")

