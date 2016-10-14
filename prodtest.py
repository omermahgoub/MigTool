import hashlib
import json

__author__ = 'OmerMahgoub'

#!/usr/bin/env python
import novaclient.v2.client as nvclient
import keystoneclient.v2_0.client as ksclient
import neutronclient.v2_0.client as neclient

import cinderclient.v2.client as ciclient
#from ceilometerclient import client
#from ceilometerclient.common import utils
import ceilometerclient.v2.client as ceiloclient

from common.ProjectDB import *


class OpenStackAdapterProjects(object):
    start_date = "2014-11-19T00:00:00"
    end_date = "2014-11-19T23:00:00"
    _objProjectDB = ProjectDB()
    #cclient = ceilometerclient.client.get_client(2, os_username='admin', os_password='AwalNet@123', os_tenant_name='stc-demo', os_auth_url='http://172.18.112.2:5000/v2.0')

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
            creds['auth_url'] = "http://172.18.112.2:5000/v2.0"
            creds['username'] = "admin"
            creds['password'] = "AwalNet@123"
            creds['tenant_name'] = projectname
            return creds
        elif service.lower() in ("nova", "cinder"):
            creds = {'username': '', 'api_key': '', 'auth_url': '', 'project_id': ''};
            creds['username'] = "stc"
            creds['api_key'] = "test1234"
            creds['auth_url'] = "http://172.18.112.2:5000/v2.0"
            creds['project_id'] = projectname
            # creds['service_type'] = "admin"
            return creds
    def get_nova_credentials(service, UserName, TenantName):
        """Returns a creds dictionary filled with the following keys:

        * username
        * password (depending on the service)
        * project_id (depending on the service)
        * auth_url

        :param service: a string indicating the name of the service
                        requesting the credentials.
        """
        try:
            if service.lower() in ("neutron"):
                creds = {'auth_url': '', 'username': '', 'password': '', 'tenant_name': ''};
                creds['auth_url'] = "http://cloudbeta.stcs.com.sa:5000/v2.0"
                creds['username'] = UserName
                creds['password'] = "test1234"
                creds['tenant_name'] = TenantName
                return creds
            elif service.lower() in ("nova"):
                creds = {'username': '', 'api_key': '', 'auth_url': '', 'project_id': ''};
                creds['username'] = UserName
                creds['api_key'] = "test1234"
                creds['auth_url'] = "http://cloudbeta.stcs.com.sa:5000/v2.0"
                creds['project_id'] = TenantName
                return creds
            elif service.lower() in ("cinder"):
                creds = {'username': '', 'api_key': '', 'auth_url': '', 'project_id': ''};
                creds['username'] = UserName
                creds['api_key'] = "test1234"
                creds['auth_url'] = "http://cloudbeta.stcs.com.sa:5000/v2.0"
                creds['project_id'] = TenantName
                return creds
        except Exception,e:
            return e.args

    def get_keystone_credentials(TenantName):
        """Returns a creds dictionary filled with the following keys:

        * username
        * password (depending on the service)
        * project_id (depending on the service)
        * auth_url

        :param service: a string indicating the name of the service
                        requesting the credentials.
        """
        try:
            creds = {'auth_url': '', 'username': '', 'password': '', 'tenant_name': ''};
            creds['auth_url'] = "http://172.18.112.2:5000/v2.0"
            creds['username'] = "admin"
            creds['password'] = "AwalNet@123"
            creds['tenant_name'] = TenantName
            return creds
        except Exception,e:
            return e.args

    kcreds = get_credentials("keystone", "admin")
    ncreds = get_credentials("nova", "stc-demo")
    necreds = get_credentials("neutron", "admin")
    ccreds = get_credentials("cinder","admin")


    novacreds = get_nova_credentials(service='nova',UserName='stc',TenantName='stc-demo')
    neutroncreds = get_nova_credentials(service='neutron',UserName='admin',TenantName='MiracleSoft15')
    cindercreds = get_nova_credentials(service='cinder',UserName='mamerpasha3',TenantName='MiracleSoft15')
    ceilocreds = get_keystone_credentials('StatsProject')


    _objkeystone = ksclient.Client(**kcreds)
    _objnova = nvclient.Client(**ncreds)
    _objneutron = neclient.Client(**necreds)
    _objcinder = ciclient.Client(**ccreds)
    _objCeilo = ceiloclient.Client('http://172.18.112.2:8777/',**ceilocreds)

    _objNovaTest = nvclient.Client(**novacreds)
    _objNeutronTest = neclient.Client(**neutroncreds)
    _objCinderTest = ciclient.Client(**cindercreds)
    #_objCeiloNew = ceilometerclient.client.get_client(2, os_username='admin', os_password='AwalNet@123', os_tenant_name='stc-demo', os_auth_url='http://172.18.112.2:5000/v2.0')


    def Project_Availability(self, ProjectName):
        """
        :param ProjectName: a string indicating the name of the Project
                        requesting the Project Availability.
        """
        tenantId = ""
        tenant_lists = self._objkeystone.tenants.list()
        #print tenant_lists

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
            self._objkeystone.tenants.create(ProjectName, description=None, enabled=True)
            message = {'Status': True}
            return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            errMsg = "Tenant Name: %s and Error is %s " % (ProjectName, message)
            # self._objLogs.Logger("CreateProject", 'critical', errMsg)
            return message



    def UpdateExistingProjectQuotas(self, ProjectName):
        #try:
       # print PlanData
        tenant_lists = self._objkeystone.tenants.list()

        for tenant in tenant_lists:
            if tenant.name == ProjectName:
                tenantId = tenant.id

        # GetProjectQuota = self._objnova.quotas.get(tenantId)
        # GetNetworkQuota = self._objneutron.show_quota(tenantId)
        #
        # print GetProjectQuota
        # print GetProjectQuota
        # PlanData['instances'] = int(GetProjectQuota['QuotaDetails'].instances) + int(PlanData['instances'])
        # PlanData['cores'] = int(GetProjectQuota['QuotaDetails'].cores) + int(PlanData['cores'])
        # PlanData['ram'] = int(GetProjectQuota['QuotaSet'].ram) + int(PlanData['ram'])
        #
        #
        #
        # Plan_Keys = ['instances', 'cores', 'ram']
        # Quota_Info = dict(zip(Plan_Keys, itemgetter(*Plan_Keys)(PlanData)))
        #
        # NetworkUpdatePlanData = {'quota': {'subnet': 1 + GetNetworkQuota['quota']['subnet'], 'network': 1 + GetNetworkQuota['quota']['network'],
        #                      'floatingip': 1 + GetNetworkQuota['quota']['floatingip'], 'security_group_rule': 3 + GetNetworkQuota['quota']['security_group_rule'],
        #                      'security_group': 1 + GetNetworkQuota['quota']['security_group'], 'router': 1 + GetNetworkQuota['quota']['router'],
        #                      'port': 3 + GetNetworkQuota['quota']['port']}}

        # self._objneutron.update_quota(tenantId, NetworkUpdatePlanData)
        Quota_Info = {'instances': 2, 'ram': 4096, 'cores': 8}
        self._objnova.quotas.update(tenantId, **Quota_Info)

            # return Quota_Info
        message = {'Status': True}
        return message
        # except Exception, e:
        #     message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
        #     errMsg = "Tenant Name: %s and Error is %s " % (ProjectName, message)
        #     self._objLogs.Logger("UpdateExistingProjectQuotas", 'critical', errMsg)
        #     return message

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

    def AssignUsertoProject(self, UserName, CustomerId):
        try:
            #strCustomerInfo = self._objProjectDB.GetTenantIdByCustomerId(CustomerId)
            tenantId = "10de37d9c1eb44698c7c5215e2f16692"

            print "printing from Assign Function %s" % UserName

            superUser = self.get_user_id("admin01")
            normalUser = self.get_user_id(UserName)


            print "Printing Admin & User Info", superUser, normalUser

            admin_role = self.GetRole("admin")
            admin_list_roles = self._objkeystone.users.list_roles(superUser, tenant=tenantId)

            print "Printing Admin Role %s" % admin_role

            user_role = self.GetRole("_member_")
            user_list_roles = self._objkeystone.users.list_roles(superUser, tenant=tenantId)

            print "Printing User Role %s" % user_role

            msgStatus = False
            for roleId in admin_list_roles:
                if roleId.id == admin_role:
                    msgStatus = True

            if msgStatus:
                print "Admin Role Already There %s", msgStatus
            else:
                self._objkeystone.roles.add_user_role(superUser, admin_role, tenant=tenantId)
                print "Admin Role New Assigned"

            msgUserStatus = False
            for roleId in user_list_roles:
                if roleId.id == admin_role:
                    msgUserStatus = True

            if msgUserStatus:
                print "User Role Already There %s", msgUserStatus
            else:
                self._objkeystone.roles.add_user_role(normalUser, user_role, tenant=tenantId)
                print "User Role New Assigned"

            message = {'Status': True}

            print "Super User & Regular User Assigned Successfully"
            return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            errMsg = "User Name: %s and Error is %s " % (UserName, message)
            #self._objLogs.Logger("AssignUsertoProject", 'critical', errMsg)
            return message

    def CreateUser(self, tenantUserName, CustomerId):
        try:
            #strCustomerInfo = self._objProjectDB.GetTenantIdByCustomerId(CustomerId)
            tenantId = "10de37d9c1eb44698c7c5215e2f16692"

            self._objkeystone.users.create(name=tenantUserName, password="test1234",
                                   email=None, tenant_id=tenantId)

            roleId = self.GetRole("_member_")

            self._objkeystone.roles.add_user_role(tenantUserName, roleId, tenantId)

            message = {'Status': True}
            return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            errMsg = "User Name: %s and Error is %s " % (tenantUserName, message)
            #self._objLogs.Logger("CreateProject", 'critical', errMsg)
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

    def Create_KeyPair(self,KeyName):
        # keycreds = self._objnova.keypairs.create("zubair_key123")
        # novacreds = self.get_nova_creds()
        # nova = nvclient.Client(**novacreds)
        # keystone1 = ksclient.Client(**keycreds)
        #self._objNovaTest.keypairs.create("Zubair_Key")

        #nova.keypairs.list()
        #_objNovaTest = self.get_nova_credentials('nova','mamerpasha3','MiracleSoft15')
        self._objNovaTest.keypairs.cr

        return self._objNovaTest.images.list()



    def Authenticate(self):
        print self._objNeutronTest.list_security_group_rules()

    def GetExactTenantNameByUserName(self, CustomerId):

        strCustomerInfo = self._objProjectDB.GetTenantIdByCustomerId(CustomerId)
        dbtenantId = strCustomerInfo['TenantId']


        tenant_lists = self._objkeystone.tenants.list()
        #
        tenantName = ""
        for tenant in tenant_lists:
            if tenant.id == dbtenantId:
                tenantName = tenant.name

        print tenantName

    def Security_Group_Rules(self):
        print self._objNeutronTest.list_security_group_rules()

    def Security_Group(self):
        list_groups = self._objNeutronTest.list_security_groups()
        #print list_groups
        #print type(list_groups)

        # for key, value in list_groups.iteritems():
        #     print value[key]
        security_group_id = ""

        for groups in list_groups.iterkeys():
            groupvalues = list_groups[groups]
            for lstGroup in groupvalues:
                if lstGroup['name'] == 'default':
                    security_group_id = lstGroup['id']
        return security_group_id

    def Add_Security_Rule(self):
        group_id = self.Security_Group()
        RuleData  = {'security_group_rules':[{'remote_group_id': None,'direction': 'egress','remote_ip_prefix': '0.0.0.0/0','protocol': 'tcp',
                                              'tenant_id': '9aa3925c9f204f4d8f7c84326418c85d','port_range_max': 900,
                                              'security_group_id': group_id,'port_range_min': 900,'ethertype': 'IPv4'}]}
        print self._objNeutronTest.create_security_group_rule(body=RuleData)


    def Storage_Issues(self):
        tenant_id = '9aa3925c9f204f4d8f7c84326418c85d'
        #print self._objCinderTest.quotas.get(tenant_id)
        CurrentQuota =  self._objcinder.quotas.get(tenant_id)

        #json_body = {"quota_set": {"volumes": 12}}
        print CurrentQuota
        print "Volumes %s" % CurrentQuota.volumes


        #print CurrentQuota.QuotaSet.backup_gigabytes

        Storage_Quota_Info = {'volumes':5}




        #print self._objcinder.quotas.update(tenant_id, **Storage_Quota_Info)
        #self._objCinderTest.quotas.update()

    def GetStorageQuotaInfoByTenantId(self, tenantId):
        try:
            return {'Status': True, 'QuotaDetails': self._objcinder.quotas.get(tenantId)}
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            errMsg = "Tenant Name: %s and Error is %s " % (tenantId, message)
            self._objLogs.Logger("GetQutotaInfoByTenantId", 'critical', errMsg)
            return message

    def GetNetworkQutotaInfoByTenantId(self, tenantId):
        try:
            return {'Status': True, 'QuotaDetails': self._objneutron.show_quota(tenantId)}
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            errMsg = "Tenant Name: %s and Error is %s " % (tenantId, message)
            self._objLogs.Logger("GetQutotaInfoByTenantId", 'critical', errMsg)
            return message

    def UpdateAddonProjectQuotas(self, Cust_TenantId, Addon_Type, Quantity):
        print Addon_Type
        if Addon_Type == 'Storage':
            GetStorageQuota = self.GetStorageQuotaInfoByTenantId(Cust_TenantId)
            current_volumes = GetStorageQuota['QuotaDetails'].volumes
            current_disk = GetStorageQuota['QuotaDetails'].gigabytes

            print "Current Volumes and Storage %s,%s" %(current_volumes,current_disk)

            print Addon_Type

            if GetStorageQuota['Status'] not in ('Error', False):
                Storage_Quota_Info = {'volumes':current_volumes + 1, 'gigabytes': current_disk + Quantity}

                updatedQuota = self._objcinder.quotas.update(Cust_TenantId, **Storage_Quota_Info)

                # return Quota_Info
                print "After Update %s,%s" % (updatedQuota.volumes, updatedQuota.gigabytes)
                message = {'Status': True}
                print "Update message", message
                return message

        elif Addon_Type == "FloatingIP":
            GetNetworkQuota = self.GetNetworkQutotaInfoByTenantId(Cust_TenantId)

            NetworkUpdatePlanData = {'quota': {'floatingip': Quantity + GetNetworkQuota['QuotaDetails']['quota']['floatingip']}}

            return self._objneutron.update_quota(Cust_TenantId, NetworkUpdatePlanData)

    def Get_TenantId(self):
        try:
            #print UserName
            print "Zubair"
            User_Check = self._objkeystone.tenants.list()
            print User_Check
            #
            if User_Check == "":
                message = {'Status': False}
                return message
            else:
                message = {'Status': True}
                return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': e.args}
            return message

    def Create_VM(self):
        try:
            imagelist = self._objNovaTest.images.find(name='Centos-6')
            flavorlist = self._objNovaTest.flavors.find(name='General purpose - Plan 2')
            #return imagelist
            print imagelist
            print flavorlist
            #return self._objNovaTest.servers.create(name='VM10', image=imagelist,
            #                                   flavor=flavorlist, key_name=None, nics=[{'net-id': '81a1ba70-7303-4763-b791-9ed50a58cff8'}])
        except Exception, e:
            print str(e)

    def Metering(self):

        #query = [dict(field='resource_id', op='eq', value='cf879910-90fc-4da5-8b81-26f681b5e736'), dict(field='meter',op='eq',value='instance:General purpose - Plan 1')]
        # queryold = [dict(field='resource_id', op='eq', value='62f2622f-dd06-42c7-afd5-d64542dd7e81'),dict(field='timestamp', op='ge', value='2015-08-19T07:27:31'),
        #             dict(field='timestamp', op='lt', value='2015-08-19T10:27:31')]
        # resultold =  self._objCeilo.statistics.list(meter_name='instance:General purpose - Plan 1',q=queryold)
        #
        # print "The Result is %s" % resultold
        # exit()
        # #[dict(field='resource_id', op='eq', value='62f2622f-dd06-42c7-afd5-d64542dd7e81'),
        # query =  [dict(field='resource_id', op='eq', value='62f2622f-dd06-42c7-afd5-d64542dd7e81')]
        #          #dict(field='timestamp', op='ge', value='2015-08-19T07:27:31'),
        #          #dict(field='timestamp', op='lt', value='2015-08-19T10:27:31')]
        #
        # result = self._objCeilo.statistics.list(meter_name='instance:General purpose - Plan 1',q = query, period = 600)
        # print result
        #
        # #query1 = [dict(field='resource_id', op='eq', value='62f2622f-dd06-42c7-afd5-d64542dd7e81'), dict(field='meter',op='eq',value='cpu_util')]
        # #result1 = self._objCeilo.samples.list(meter_name = 'instance:General purpose - Plan 1',q=query1, limit = 2)
        #
        # # result1 = self._objCeilo.new_samples.list(q=query1)
        # #print result1

        """" For Statistics """""
        #instance:Workload-Optimized - Plan 1
        queryold = [dict(field='resource_id', op='eq', value='f951d16f-7702-43b0-bc57-46f27e09c0c6'),
                    dict(field='timestamp', op='ge', value='2015-08-22T09:50:30'),
                    dict(field='timestamp', op='lt', value='2015-08-23T09:50:30')]
        #resultold =  self._objCeilo.statistics.list(meter_name='instance:General purpose - Plan 2', q=queryold, groupby = {'resource_id':'f951d16f-7702-43b0-bc57-46f27e09c0c6'})

        #print "Result %s" % resultold
        #exit()

        """"""""""""""""""""""""" New Code"""""""""""""""""""""""""""""""""""""""
        # inst_list = list()
        # meters_list = self._objCeilo.meters.list()
        # [inst_list.append(meters.resource_id) for meters in meters_list if meters.name == 'instance']
        # print inst_list
        #
        #
        # instances_server = list()
        # for instance in inst_list:
        #     query = [dict(field='timestamp', op='gt', value=self.start_date),
        #              dict(field='timestamp', op='lt', value=self.end_date),
        #              dict(field='resource', op='eq', value=instance)]
        #     samples = self._objCeilo.samples.list(meter_name='instance',
        #                               q=query,
        #                               limit=1)
        #     if samples:
        #         hash1 = hashlib.sha224(samples[0].project_id + 'node-37.cloudbeta.stcs.com.sa')
        #         hash1 = hash1.hexdigest()
        #         if hash1 == samples[0].resource_metadata['host']:
        #             instances_server.append(samples[0].resource_id)
        #     print instances_server
        # exit()


        #return inst_list


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        #querynew = [dict(field='project', op='eq', value='56b07d1584ed4addb1b2956dcf3cb987'),dict(field='meter',op='eq',value='cpu_util')]
        querynew = [{"field": "timestamp","op": "ge","value": "2015-08-24T00:00:00"},{"field": "timestamp","op": "lt","value": "2015-08-25T00:00:00"},
                    {"field": "resource_id","op": "eq","value": "eb07bdda-a214-4053-8f36-5e4d752691b6"},
                    {"field": "meter","op": "eq","value": "instance:m1.medium"}]

        #resultnew = self._objCeilo.meters.list(q=querynew)
        #resultnew = self._objCeilo.samples.list(q=querynew)

        query_statistics = [{'field': 'resource', 'op': 'eq', 'value': 'eb07bdda-a214-4053-8f36-5e4d752691b6'},
                            {'field': 'timestamp', 'op': 'gt', 'value': '2015-08-24T10:09:00'},
                            {'field': 'timestamp', 'op': 'lt', 'value': '2015-08-24T19:00:00'}]

        instance_duration = ''
        duration = self._objCeilo.statistics.list(meter_name='instance', q=query_statistics)
        for seconds in duration:
            duration_parsed = json.loads(json.dumps(seconds.to_dict()))
            duration_output = json.loads(json.dumps(duration_parsed, indent=4, sort_keys = True))
            instance_duration = str(duration_output['duration'])

        print "++++++++++++Instance Duration++++++++++"

        print instance_duration

        print "++++++++++++New Results++++++++++"
        #print resultnew
        exit()
        """" End of Statistics """""



#
objTest = OpenStackAdapterProjects()
print objTest.Metering()
# objTest.Storage_Issues()
#print objTest.UpdateAddonProjectQuotas('9aa3925c9f204f4d8f7c84326418c85d','FloatingIP',1)
#print objTest.Get_TenantId()
# print objTest.Create_VM()

#print objTest.Create_KeyPair('test')
#print objTest.Security_Group()
# print objTest.Security_Group_Rules()
#print objTest.Add_Security_Rule()
#print objTest.Storage_Issues()
# GetStorageQuota = objTest.GetStorageQuotaInfoByTenantId('9aa3925c9f204f4d8f7c84326418c85d')
# print GetStorageQuota
# print GetStorageQuota['QuotaDetails'].volumes



#objTest.GetExactTenantNameByUserName(20)
# keylist = objTest.Create_KeyPair("test")
# print keylist[0]


#print objTest.CreateUser("mpashabhai",20)
#print objTest.User_Availability("miqbal12")
#print objTest.AssignUsertoProject("mzubair",20)


# print objTest.Project_Availability("admin")
#print objTest.CreateProject("Zubi Bhai19")
#PlanData = {'Zone': 'nova-ruh-highend-zone', 'Image': 'TestVM', 'ram': 1024, 'instances': '1', 'cores': u'4', 'Flavor': 'm1.large'}
# print objTest.UpdateExistingProjectQuotas("Zubi Bhai19")