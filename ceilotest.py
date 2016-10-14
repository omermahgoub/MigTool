import hashlib
import json
import datetime

__author__ = 'OmerMahgoub'

#!/usr/bin/env python
import novaclient.v2.client as nvclient
import keystoneclient.v2_0.client as ksclient

import ceilometerclient.v2.client as ceiloclient

class OpenStackAdapterProjects(object):
    def get_keystone_credentials(TenantName):
        try:
            creds = {'auth_url': '', 'username': '', 'password': '', 'tenant_name': ''};
            creds['auth_url'] = "http://172.18.112.2:5000/v2.0"
            creds['username'] = "admin"
            creds['password'] = "AwalNet@123"
            creds['tenant_name'] = TenantName
            return creds
        except Exception,e:
            return e.args

    ceilocreds = get_keystone_credentials('StatsProject')
    _objCeilo = ceiloclient.Client('http://172.18.112.2:8777/',**ceilocreds)

    def get_current_date_and_time(self):
        get_date_and_time = datetime.datetime.now()
        current_date_and_time = get_date_and_time.strftime('%Y-%m-%dT%H:%M')
        print current_date_and_time
        return current_date_and_time

    def get_beginning_of_current_month(self):
        get_first_day_of_month = datetime.datetime.now()
        first_day_of_month = get_first_day_of_month.strftime('%Y-%m-01T00:00')
        print first_day_of_month
        return first_day_of_month

    def Metering(self):
        # get_data_end = self.get_current_date_and_time()
        # get_data_start = self.get_beginning_of_current_month()
        #
        # os_tenant_id = '7ea28ffeade94615a5f1b7a1d6c73aa4'
        # os_tenant_name ='StatsProject'
        # query_resource_detail = [{'field': 'project', 'op': 'eq', 'value': os_tenant_id},{'field': 'source', 'op': 'eq', 'value': 'openstack'}]
        # instance_duration = ''
        # query_statistics = [{'field': 'resource_id', 'op': 'eq', 'value': 'eb07bdda-a214-4053-8f36-5e4d752691b6'},{'field': 'timestamp', 'op': 'gt', 'value': get_data_end},
        #                     {'field': 'timestamp', 'op': 'lt', 'value': get_data_end}]
        # duration = self._objCeilo.statistics.list(meter_name='instance', q=query_statistics)
        #
        # print "Duration %s" % duration
        # exit()
        # for seconds in duration:
        #     duration_parsed = json.loads(json.dumps(seconds.to_dict()))
        #     duration_output = json.loads(json.dumps(duration_parsed, indent=4, sort_keys = True))
        #     instance_duration = str(duration_output['duration'])
        # # for resource in self._objCeilo.resources.list(q=query_resource_detail):
        # #     resources_parsed = json.loads(json.dumps(resource.to_dict()))
        # #     resources_output = json.loads(json.dumps(resources_parsed, indent=4, sort_keys = True))
        # #     my_id = resources_output['resource_id']
        # #
        # #     if not resources_output['resource_id'].startswith('instance-') and not resources_output['resource_id'].endswith('-vda') and resources_output['user_id']:
        # #         resource_display_name = ''
        # #
        # #
        # #         # Now getting resource details
        # #         query_instance_details = [{'field': 'resource', 'op': 'eq', 'value': my_id}]
        # #         resource_details = self._objCeilo.resources.get(my_id)
        # #         resource_details_parsed = json.loads(json.dumps(resource_details.to_dict()))
        # #         resource_details_output = json.loads(json.dumps(resource_details_parsed, indent=4, sort_keys = True))
        # #         print resource_details_output
        # #         exit()
        #         #
        #         # if 'OS-EXT-AZ:availability_zone' or 'availability_zone' in resource_details_output['metadata']:
        #         #     if 'display_name' in  resource_details_output['metadata']:
        #         #         resource_display_name = resource_details_output['metadata']['display_name']
        #         #     if 'status' in resource_details_output['metadata']:
        #         #         resource_status = resource_details_output['metadata']['status']
        #        #     if 'state' in resource_details_output['metadata']:
        #        #         resource_status = resource_details_output['metadata']['state']
        #        #
        #        #     print resource_status
        #        #
        #        #     # No we will get some statistics for an instance.
        #        #     query_statistics = [{'field': 'resource', 'op': 'eq', 'value': my_id},{'field': 'timestamp', 'op': 'gt', 'value': get_data_end},{'field': 'timestamp', 'op': 'lt', 'value': get_data_end}]
        #        #
        #        #
        #        #     # For instance duration
        #        #     instance_duration = ''
        #        #     duration = self._objCeilo.statistics.list(meter_name='instance', q=query_statistics)
        #        #     for seconds in duration:
        #        #         duration_parsed = json.loads(json.dumps(seconds.to_dict()))
        #        #         duration_output = json.loads(json.dumps(duration_parsed, indent=4, sort_keys = True))
        #        #         instance_duration = str(duration_output['duration'])
        #        #
        #        #     collected_resource_data = resources_output['project_id'] + ";" + os_tenant_name + ";" + resources_output['resource_id'] + ";" + resource_display_name + ";" + resource_status + ";" + instance_duration + ";" + vcpu_average + ";" + memory_average + ";" + disk_root_average + ";" + disk_ephemeral_average
        #        #     print collected_resource_data
        #        # else:
        #        #     print "System seems not be a virtiual machine."







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

objTest = OpenStackAdapterProjects()
print objTest.Metering()
