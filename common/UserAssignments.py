__author__ = 'OmerMahgoub'

#!/usr/bin/env python
import novaclient.v2.client as nvclient
import keystoneclient.v2_0.client as ksclient

from common.Auth import OpenStackAdapterAuth as OpenStackAuth
from common.ProjectDB import *
from settings import settings
import Logger


class OpenStackAdapterUsers(object):

    objSettings = settings.StackSettings()
    usercfgSettings = objSettings.ServiceSettings("UserSettings")

    objAuth = OpenStackAuth()
    kcreds = objAuth.get_credentials("keystone","admin")
    ncreds = objAuth.get_credentials("nova","admin")


    _objkeystone = ksclient.Client(**kcreds)
    _objnova = nvclient.Client(**ncreds)
    _objProjectDB = ProjectDB()
    _cfgDefaultPasswd = usercfgSettings["DefaultUserPassword"]

    _objLogs = Logger.VMLogger()

    """  User Association & Disassociation Process Starts """

    def User_Availability(self, UserName):
        try:
            print UserName
            User_Check = self._objkeystone.users.find(name=UserName)

            if User_Check == "":
                message = {'Status': False}
                return message
            else:
                message = {'Status': True}
                return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            return message

    #self.CreateUser(UserName, TenantId)
    def CreateUser(self, tenantUserName, TenantId):
        try:
            # strCustomerInfo = self._objProjectDB.GetTenantIdByCustomerId(CustomerId)
            # tenantId = strCustomerInfo['TenantId']

            self._objkeystone.users.create(name=tenantUserName, password=self._cfgDefaultPasswd,
                                   email=None, tenant_id=TenantId)

            roleId = self.GetRole("_member_")

            self._objkeystone.roles.add_user_role(tenantUserName, roleId, TenantId)

            message = {'Status': True}
            return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            errMsg = "User Name: %s and Error is %s " % (tenantUserName, message)
            self._objLogs.Logger("CreateProject", 'critical', errMsg)
        return message



    def CreateKeyPair(self, CustomerName, UserName):
        try:
            objAuth = OpenStackAuth()
            usercreds = objAuth.get_nova_neutron_credentials("nova", UserName, CustomerName)
            nova = nvclient.Client(**usercreds)

            nova.keypairs.create(UserName+"_key")
            message = {'Status': True}
            return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            errMsg = "User Name: %s and Error is %s " % (UserName, message)
            self._objLogs.Logger("CreateProject", 'critical', errMsg)
        return message

    #AssignUsertoProject(UserName, TenantId)
    def AssignUsertoProject(self, UserName, TenantId):
        try:
            # strCustomerInfo = self._objProjectDB.GetTenantIdByCustomerId(CustomerId)
            # tenantId = strCustomerInfo['TenantId']

            print "printing from Assign Function %s" % UserName

            superUser = self.get_user_id("admin01")
            normalUser = self.get_user_id(UserName)


            print "Printing Admin & User Info", superUser, normalUser

            admin_role = self.GetRole("admin")
            admin_list_roles = self._objkeystone.users.list_roles(superUser, tenant=TenantId)

            user_role = self.GetRole("_member_")
            user_list_roles = self._objkeystone.users.list_roles(normalUser, tenant=TenantId)

            msgStatus = False
            for roleId in admin_list_roles:
                if roleId.id == admin_role:
                    msgStatus = True

            if msgStatus:
                print "Admin Role Already There %s", msgStatus
            else:
                self._objkeystone.roles.add_user_role(superUser, admin_role, tenant=TenantId)

            msgUserStatus = False
            for roleId in user_list_roles:
                if roleId.id == user_role:
                    msgUserStatus = True

            if msgUserStatus:
                print "User Role Already There %s", msgUserStatus
            else:
                self._objkeystone.roles.add_user_role(normalUser, user_role, tenant=TenantId)

            message = {'Status': True}

            print "Super User & Regular User Assigned Successfully"
            return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            errMsg = "User Name: %s and Error is %s " % (UserName, message)
            self._objLogs.Logger("AssignUsertoProject", 'critical', errMsg)
            return message

    def DisassociateUserFromProject(self, ProjectName):
        try:

            tenantId = ""
            tenant_lists = self._objkeystone.tenants.list()
            for tenant in tenant_lists:
                if tenant.name == ProjectName:
                    tenantId = tenant.id
            if tenantId == "":
                message = {'Status': False}
                return message
            else:
                message = {'Status': True}

                roleId = self.GetRole("_member_")

                print "printing from Diassociation Function %s" % ProjectName

                superUser = self.get_user_id("superadmin")

                self._objkeystone.tenants.remove_user(tenantId, superUser, roleId)

                return message

        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            errMsg = "User Name: %s and Error is %s " % (ProjectName, message)
            self._objLogs.Logger("CreateProject", 'critical', errMsg)
            return message

    def GetRole(self, RoleName):
        try:

           roles_list = self._objkeystone.roles.list()
           for role in roles_list:
                if role.name == RoleName:
                    roleId = role.id
           return roleId
        except:
            return None

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

    """  User Association & Disassociation Process Ends """
    #(CustomerId, CustomerName, UserName)
    def AssignUserQueue(self, CustomerId, CustomerName, UserName, TenantId):
        try:
            """"Initialization of Connection """""
            self._objLogs.Logger("AssignUserQueue", "info", "Create User Started")



            # Check User Availability
            print "User Creation Process Initiated"
            chk_avail = self.User_Availability(UserName)
            print "Chk_Avail %s" % chk_avail
            self._objLogs.Logger("UserAvailability", "info", "User Exists %s" % chk_avail)
            self._objLogs.Logger("UserAvailability", "info", "Username %s" % UserName)

            if chk_avail['Status'] != 'Error':
                print "Is the User Existing? %s" % chk_avail
                if chk_avail['Status'] == True:
                    print "Assignation Process Initiated for User %s" % UserName
                    print("User Already Exists.Now Assigning User to the Project")

                    # Assign the User to the Project
                    userStatus = self.AssignUsertoProject(UserName, TenantId)
                    print "Printing User Status %s ", userStatus

                    self._objLogs.Logger("UserAssignQueue", "info", "User Assignation Process Completed")

                    if userStatus['Status'] not in ('Error',False):
                        if userStatus['Status'] == False:
                            message = {'Status': False}
                        else:
                            message = {'Status': True}
                        return message
            elif chk_avail['Status'] == 'Error':
                # New Customer
                # Create New Project
                print("Creating New User under the Project %s" %  + CustomerId)

                strUserCreation = self.CreateUser(UserName, TenantId)

                print "User Creation %s" % strUserCreation['Status']
                if strUserCreation['Status'] not in ('Error',False):
                    print "Creating Key Pair %s" % UserName+"_key"
                    strKeyPairCreation = self.CreateKeyPair(CustomerName, UserName)
                    print "Key Pair Status %s" % strKeyPairCreation['Status']


                    message = {'Status': True}
                else:
                    message = {'Status': False}
                    return message

                self._objLogs.Logger("CreateUserQueue", "info", "User Created %s" % "prj_" + UserName)
                self._objLogs.Logger("CreateUserQueue", "info", "User Creation Process Completed")
            else:
                template = "An exception of type {0} occurred. Details are:\n{1!r}. Parameters are:\n{2!r}"
                message = template.format(chk_avail['Type'], chk_avail['Message'], UserName)

                self._objLogs.Logger("AssignUserQueue", "critical", message)
                message = {'Status': 'Error'}
            return message
        except Exception, e:
            template = "An exception of type {0} occurred. Details are:\n{1!r}."
            message = template.format(type(e).__name__, e.args)
            self._objLogs.Logger("AssignUserQueue", "critical", message)
            return {'Status': 'Error'}

