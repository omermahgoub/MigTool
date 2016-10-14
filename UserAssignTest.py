__author__ = 'OmerMahgoub'
#!/usr/bin/env python
import random
from keystoneclient.v2_0 import Client as k_client
import novaclient.v2.client as nvclient
import keystoneclient.v2_0.client as ksclient
import neutronclient.v2_0.client as neclient
from operator import itemgetter
from Logger import VMLogger
import settings
from settings import settings

class UserTest:

    objSettings = settings.StackSettings()
    cfgSettings = objSettings.ServiceSettings("OpenStack")

    _cfgHostName = cfgSettings["host"]
    _cfgUserId = cfgSettings["user"]
    _cfgStackPwd = cfgSettings["passwd"]
    _cfgTenantName = cfgSettings["tenantName"]

    def get_credentials(self,service, projectname):
        if service.lower() in ("keystone", "neutron"):
            creds = {'auth_url': '', 'username': '', 'password': '', 'tenant_name': ''};
            creds['auth_url'] = self._cfgHostName
            creds['username'] = self._cfgUserId
            creds['password'] = self._cfgStackPwd
            creds['tenant_name'] = projectname
            return creds
        elif service.lower() in ("nova", "cinder"):
            creds = {'username': '', 'api_key': '', 'auth_url': '', 'project_id': ''};
            creds['username'] = self._cfgUserId
            creds['api_key'] = self._cfgStackPwd
            creds['auth_url'] = self._cfgHostName
            creds['project_id'] = projectname
            return creds

    """  User Association & Disassociation Process Starts """

    def AssignUsertoProject(self, ProjectName, UserId):
        # try:
        kcreds = self.get_credentials("keystone","admin")
        _objkeystone = ksclient.Client(**kcreds)

        tenantId = ""
        tenant_lists =_objkeystone.tenants.list()
        for tenant in tenant_lists:
            if tenant.name == ProjectName:
                tenantId = tenant.id
        if tenantId == "":
            message = {'Status': False}
            return message
        else:
            message = {'Status': True}

            AdminRole = self.GetRole("_member_")
            UserRole = self.GetRole("_member_")
            print AdminRole
            print UserRole

            print "printing from Assign Function %s" % UserId
            superUser = self.get_user_id("admin01")
            print "Super User %s", superUser

            print _objkeystone.roles.add_user_role(superUser,AdminRole,tenant=tenantId)
            print _objkeystone.roles.add_user_role(UserId,UserRole,tenant=tenantId)

            # _objkeystone.users.update_tenant(UserId, tenantId)
            # _objkeystone.users.update_tenant(user= UserId,tenant=tenantId)
            # _objkeystone.users.update_tenant(superUser, tenantId)



            print "Super User Assigned Successfully"
            return message
        # except Exception, e:
        #     message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
        #     errMsg = "User Name: %s and Error is %s " % (UserId, message)
        #     self._objLogs.Logger("AssignUsertoProject", 'critical', errMsg)
        #     return message

    def GetRole(self, RoleName):
        try:
           kcreds = self.get_credentials("keystone","admin")
           _objkeystone = ksclient.Client(**kcreds)

           roles_list = _objkeystone.roles.list()
           for role in roles_list:
                if role.name == RoleName:
                    roleId = role.id
           return roleId
        except:
            return None

    def get_user_id(self,Uname):
        try:
            kcreds = self.get_credentials("keystone","admin")
            _objkeystone = ksclient.Client(**kcreds)
            userId = ""
            users_lists = _objkeystone.users.list()
            for username in users_lists:
                if username.name == Uname:
                    userId = username.id
            return userId
        except Exception, e:
            return e.args


objTest = UserTest()

print objTest.AssignUsertoProject("Ghulam1","89fda8df2b59472bb8c132fa4c63aa26")
print objTest.AssignUsertoProject("Ghulam2","89fda8df2b59472bb8c132fa4c63aa26")
print objTest.AssignUsertoProject("Ghulam3","89fda8df2b59472bb8c132fa4c63aa26")
# print objTest.AssignUsertoProject("Ghulam04","89fda8df2b59472bb8c132fa4c63aa26")
# print objTest.AssignUsertoProject("Ghulam05","89fda8df2b59472bb8c132fa4c63aa26")

