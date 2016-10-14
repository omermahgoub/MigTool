#!/usr/bin/env python
import novaclient.v2.client as nvclient
import keystoneclient.v2_0.client as ksclient
from operator import itemgetter
#
class OpenStackAdapterProjects(object):
#
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
            #creds['auth_url'] = "http://172.18.112.2:5000/v2.0"
            creds['auth_url'] = "http://labstack.stcas.com.sa:5000/v2.0"
            creds['username'] = "superadmin"
            creds['password'] = "test1234"
            creds['tenant_name'] = "admin"
            return creds
        elif service.lower() in ("nova", "cinder"):
            creds = {'username': '', 'api_key': '', 'auth_url': '', 'project_id': ''};
            creds['username'] = "superadmin"
            creds['api_key'] = "test1234"
            creds['auth_url'] = "http://labstack.stcas.com.sa:5000/v2.0"
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

    def UpdateProjectQuotas(self, ProjectName, **PlanData):
        try:

            tenant_lists = self._objkeystone.tenants.list()
            print tenant_lists

            for tenant in tenant_lists:
                if tenant.name == ProjectName:
                    tenantId = tenant.id
            #'key_pairs':'1','Networks':'1','Ports':'1','Routers':'1','subnets':'1'

            PlanData = {'Flavor': 'm1.tiny', 'Image': 'TestVM', 'Zone': 'nova-ruh-highend-zone',
            'instances': '1', 'cores': '1', 'ram': 1 * 1024, 'floating_ips': '1','key_pairs':'1'}

            Plan_Keys = ['instances', 'cores', 'ram', 'floating_ips','key_pairs']
            Quota_Info = dict(zip(Plan_Keys, itemgetter(*Plan_Keys)(PlanData)))

            # body_sample = {'quota_items': {'quota_network': 1,'quota_port': 1,
            #                        'quota_subnet': 1}}
            print Quota_Info
            # self._objnova.quotas.update(tenantId, **Quota_Info)
            # self._objneutron.update_quota(tenantId, body_sample)
            # return Quota_Info
            message = {'Status': True}
            return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            errMsg = "Project Name: %s and Error is %s " % (ProjectName, message)
            self._objLogs.Logger("UpdateProjectQuotas", 'critical', errMsg)
            return message

    def AssignUsertoProject(self, ProjectName):
        try:
            tenantId = ""
            tenant_lists =self._objkeystone.tenants.list()
            #print tenant_lists
            for tenant in tenant_lists:
                if tenant.name == ProjectName:
                    tenantId = tenant.id
            if tenantId == "":
                message = {'Status': False}
                return message
            else:
                message = {'Status': True}

                # roleId = self.GetRole("_member_")

                #print "printing from Assign Function %s", "admin"
                superUser = self.get_user_id("admin01")
                print superUser
                #print "Super User %s", superUser
                # self._objkeystone.users.update_tenant(UserId, tenantId)
                # self._objkeystone.users.update_tenant(superUser, tenantId)

                admin_role = self.GetRole("admin")
                #print "AdminRole %s", admin_role
                #UserRole = self.GetRole("_member_")
                list_roles = self._objkeystone.users.list_roles(superUser, tenant=tenantId)

                print list_roles

                #print list_roles

                #print list_roles[0].id

                msgStatus = False
                for roleId in list_roles:
                    if roleId.id == admin_role:
                        msgStatus = True
                        #self._objkeystone.roles.add_user_role(superUser, admin_role, tenant=tenantId)
                    #self._objkeystone.roles.add_user_role(superUser, admin_role, tenant=tenantId)

                if msgStatus:
                    print "Role Already There %s", msgStatus
                else:
                    self._objkeystone.roles.add_user_role(superUser, admin_role, tenant=tenantId)

                #self._objkeystone.roles.add_user_role(UserId, UserRole, tenant=tenantId)

                #print "Super User Assigned Successfully"
                return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            errMsg = "User Name: %s and Error is %s " % ("admin", message)
            #self._objLogs.Logger("AssignUsertoProject", 'critical', errMsg)
            return message
    def get_user_id(self,Uname):
        try:
            userId = ""
            users_lists = self._objkeystone.users.list()
            for username in users_lists:
                if username.name == Uname:
                    userId = username.id
            return userId
        except Exception, e:
            return e.args
    def GetRole(self, RoleName):
        try:

           roles_list = self._objkeystone.roles.list()
           for role in roles_list:
                if role.name == RoleName:
                    roleId = role.id
           return roleId
        except:
            return None
# #
objTest = OpenStackAdapterProjects()
#print objTest.Project_Availability("admin")
# print objTest.CreateProject("Zubi Bhai")
#print objTest.UpdateProjectQuotas("Zubi Bhai")
print objTest.AssignUsertoProject("prj_pphilip")

# # from keystoneclient.auth.identity import v2
# # from keystoneclient import session
# # from novaclient import client
#
# from keystoneclient.v2_0 import client
# #
# # auth = v2.Password(auth_url="http://172.18.112.2:35357/v2.0",
# #                        username="admin",
# #                        password="AwalNet@123",
# #                        tenant_name="admin")
# #
# # sess = session.Session(auth=auth)
# # nova = client.Client(version=2,auth=sess)
# #
# # print ""
# #
# #
# #
# #
# from novaclient.v2 import client
# nt = client.Client("admin", "AwalNet@123", "admin", "http://172.18.112.2:5000/v2.0", service_type="compute")
# print nt.availability_zones.list()
# # print nt.versions.list()
#
#
# # from keystoneclient.v2_0 import client
# # nt = client.Client("admin", "AwalNet@123", "admin", "http://172.18.112.2:5000/v2.0", service_type="compute")