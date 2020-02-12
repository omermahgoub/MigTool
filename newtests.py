#!/usr/bin/env python
import novaclient.v2.client as nvclient
import keystoneclient.v2_0.client as ksclient
import neutronclient.v2_0.client as neclient
from operator import itemgetter
#
class OpenStackAdapterProjects(object):
    #
    def get_credentials(service, projectname):
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
            # creds['auth_url'] = "http:///v2.0"
            creds['auth_url'] = "http:5000/v2.0"
            creds['username'] = ""
            creds['password'] = ""
            creds['tenant_name'] = ""
            return creds
        elif service.lower() in ("nova", "cinder"):
            creds = {'username': '', 'api_key': '', 'auth_url': '', 'project_id': ''};
            creds['username'] = ""
            creds['api_key'] = ""
            creds['auth_url'] = "http://.:5000/v2.0"
            creds['project_id'] = projectname
            # creds['service_type'] = ""
            return creds
            #

    kcreds = get_credentials("keystone", "")
    _objkeystone = ksclient.Client(**kcreds)

    novacreds = get_credentials("nova", "")
    _objnova = nvclient.Client(**novacreds)

    def Project_Availability(self, ProjectName):
        """
        :param ProjectName: a string indicating the name of the Project
                        requesting the Project Availability.
        """
        tenantId = ""
        tenant_lists = self._objkeystone.tenants.list()
        # print tenant_lists

        for tenant in tenant_lists:
            if tenant.name == ProjectName:
                tenantId = tenant.id
        # print self._objkeystone.auth_token
        #
        # print self._objnova.servers.list()
        # print self._objkeystone.tenants.list_users("22e4dba9d25e408f852264629252abe2")
        #
        #print self._objnova.servers.list()
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
            resultCreation = self._objkeystone.tenants.create(ProjectName, description=None, enabled=True)
            cust_tenantId = getattr(resultCreation, 'id')

            # Store the Customer Information along with Project ID
            # result = self._objProjectDB.Create_Customer_Info(CustomerId, CustomerName, cust_tenantId)

            message = {'Status': True, 'TenantId': cust_tenantId}
            return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': str(e)}
            errMsg = "Tenant Name: %s and Error is %s " % (ProjectName, message)
            # self._objLogs.Logger("CreateProject", 'critical', errMsg)
            return message


    def AssignUsertoProject(self, UserId, TenantId):
        try:
            # strCustomerInfo = self._objProjectDB.GetTenantIdByCustomerId(CustomerId)
            # tenantId = strCustomerInfo['TenantId']

            print "printing from Assign Function %s" % UserId

            superUser = self.get_user_id("")

            print "Printing Admin & User Info", superUser, UserId

            admin_role = self.GetRole("admin")
            admin_list_roles = self._objkeystone.users.list_roles(superUser, tenant=TenantId)

            user_role = self.GetRole("_member_")
            user_list_roles = self._objkeystone.users.list_roles(UserId, tenant=TenantId)

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
                self._objkeystone.roles.add_user_role(UserId, user_role, tenant=TenantId)

            message = {'Status': True}

            print "Super User & Regular User Assigned Successfully"
            return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            errMsg = "User Name: %s and Error is %s " % (UserId, message)
            # self._objLogs.Logger("AssignUsertoProject", 'critical', errMsg)
            return message

    def GetRole(self, RoleName):
        try:
            roles_list = self._objkeystone.roles.list()
            print roles_list
            for role in roles_list:
                if role.name == RoleName:
                    roleId = role.id
            return roleId
        except:
            return None

    def get_user_id(self, Uname):
        try:
            userId = ""
            users_lists = self._objkeystone.users.list()
            for username in users_lists:
                if username.name == Uname:
                    userId = username.id
            return userId
        except Exception, e:
            return e.args

    def get_user_name(self, UserId):
        try:
            uname = ""
            users_lists = self._objkeystone.users.list()
            for userid_list in users_lists:
                print userid_list.id, ",", userid_list.name
                if userid_list.id == UserId:
                    uname = userid_list.name
            return uname
        except Exception, e:
            return e.args

    def return_tenats(self):
        tenants = self._objkeystone.tenants.list()
        my_tenant = [x for x in tenants if x.name=='Mohammad2209'][0]

        user_id = self.get_user_id('')
        my_user = self._objkeystone.users.get(user_id)

        role_id = self.GetRole('admin')
        role = self._objkeystone.roles.get(role_id)

        print self._objkeystone.roles.add_user_role(my_user, role, my_tenant)

        print role

        print my_user
        print my_tenant

    def list_servers(self):
        try:
            servers_status = self._objnova.servers.list()

            print len(servers_status)

        except Exception, e:
            return e.args

    def get_neutron_credentials1(self, projectname):


        token_id = self._objkeystone.auth_token
        creds = {'endpoint_url': '', 'token': '', 'tenant_id': '', 'insecure': ''}

        auth_creds={}
        auth_creds["auth_url"] = "http://172.18.112.2:5000/v2.0"
        auth_creds["token"] = token_id
        auth_creds["tenant_id"] = projectname

        #creds['auth_url'] = "http://172.18.112.2:5000/v2.0"
        admin_client = ksclient.Client(**auth_creds)

        creds['endpoint_url'] = "http://172.18.112.2:9696/"
        creds['token'] = admin_client.auth_token
        creds['tenant_id'] = projectname
        creds['insecure'] = False


        cc = neclient.Client(**creds)
        print cc
        #return cc


        body_sample = {'network': {'name': "test_token1",
                                    'admin_state_up': True}}

        netw = cc.create_network(body=body_sample)
        net_dict = netw['network']
        network_id = net_dict['id']
        body_create_subnet = {'subnets': [{'cidr': '10.0.0.0/24',
                                           'ip_version': 4,
                                           'network_id': network_id,
                                           'name':"test_token" +'_sub'}]}
        subnet = cc.create_subnet(body=body_create_subnet)

        print netw


    #4dd8451cafb34bde84e307f2b31cd630
    def AssignUserOnly(self, tenantid, UserId):
        try:
            # strCustomerInfo = self._objProjectDB.GetTenantIdByCustomerId(CustomerId)
            # tenantId = strCustomerInfo['TenantId']

            print "printing from Assign Function %s" % UserId

            user_role = self.GetRole("_member_")
            user_list_roles = self._objkeystone.users.list_roles(UserId, tenant=tenantid)

            msgUserStatus = False
            for roleId in user_list_roles:
                if roleId.id == user_role:
                    msgUserStatus = True

            print "Message User Status %s" % msgUserStatus

            if msgUserStatus:
                print "User Role Already There %s", msgUserStatus
            else:
                self._objkeystone.roles.add_user_role(UserId, user_role, tenant=tenantid)

                username= self.get_user_name(UserId)
                #result = customer.CustomerServices.create_customer(CustomerId, CustomerName, tenantid, UserId, username, SubscriptionId, unit)
            message = {'Status': True}

            print "Normal User Assigned Successfully"
            return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            errMsg = "User Name: %s and Error is %s " % (UserId, message)
            #self._objLogs.Logger("AssignUsertoProject", 'critical', errMsg)
            return message

    def List_Servers(self, projectname):


        token_id = self._objkeystone.auth_token
        creds = {'auth_url': '', 'auth_token': '', 'tenant_id': ''}

        auth_creds={}
        auth_creds["auth_url"] = "http://172.18.112.2:5000/v2.0"
        auth_creds["token"] = token_id
        auth_creds["tenant_id"] = projectname

        #creds['auth_url'] = "http://172.18.112.2:5000/v2.0"
        admin_client = ksclient.Client(**auth_creds)

        creds['auth_url'] = "http://172.18.112.2:5000/v2.0"
        creds['auth_token'] = admin_client.auth_token
        creds['tenant_id'] = projectname

        #nv = nvclient.Client(**creds)

        objNova = nvclient.Client(**creds)

        server_count = len(objNova.servers.list())

        volume_count = len(objNova.volumes.list())

        ip_count = len(objNova.floating_ips.list())

        print server_count
        print volume_count
        print ip_count

        if (server_count == 0) & (volume_count == 0) & (ip_count == 0):
            print "Project can be deleted with out any issues"
        else:
            print "Project can't be deleted as resources exists"

        #print "Servers List %s" % nv.servers.list()



# #
objTest = OpenStackAdapterProjects()
# print objTest.Project_Availability("admin")
#print objTest.CreateProject("")
#print objTest.get_user_name('47')
#print objTest.AssignUsertoProject(47, 'd98bc63c348340d2baefac04aa0fbd2d')
#print objTest.return_tenats()
#test = objTest.get_neutron_credentials1("e867b9fbcffa4c86917029b19de9b9d5")  #e867b9fbcffa4c86917029b19de9b9d5
#test = objTest.AssignUserOnly('4dd8451cafb34bde84e307f2b31cd630', 20)
# test = objTest.List_Servers('030316c069794e7e8bad957ba9b0c6fa')
print objTest.GetRole('_member_')
# print test


