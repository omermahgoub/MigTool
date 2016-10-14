# __author__ = 'OmerMahgoub'
# strmsg = {'EventId': u'e786786', 'PlanName': u'Premimum',
#           'PlanDetails': [{u'item':
#                                {u'itemid': 1, u'name': u'Storage', u'created': u'2015-07-02T00:00:00.000Z', u'modified': u'2015-07-02T00:00:00.000Z', u'meta_data': u'metadata',
#                                 u'description': u'Storage for this plan"'}, u'id': 1, u'unit': {u'symbol': u'GB', u'id': 1, u'short_name': u'GB', u'name': u'GigaByte'}, u'quantity': u'4.0'},
#                           {u'item':
#                                {u'itemid': 1, u'name': u'RAM', u'created': u'2015-07-02T00:00:00.000Z', u'modified': u'2015-07-02T00:00:00.000Z', u'meta_data': u'metadata',
#                                 u'description': u'Memory for this plan'}, u'id': 2, u'unit': {u'symbol': u'GB', u'id': 1, u'short_name': u'GB', u'name': u'GigaByte'}, u'quantity': u'1'},
#                           {u'item':
#                                {u'itemid': 1, u'name': u'vCPU', u'created': u'2015-07-02T00:00:00.000Z', u'modified': u'2015-07-02T00:00:00.000Z', u'meta_data': u'metadata',
#                                 u'description': u'Virtual CPU for this plan'}, u'id': 2, u'unit': {u'symbol': u'', u'id': 1, u'short_name': u'', u'name': u''}, u'quantity': u'1.0'}],
#           'CustomerName': u'Mohammad Zubair Pasha'}
#
# # 1.0 vCPU
# # 1.0 GB RAM
# # 20.0 GB Storage
#
# # print strmsg['PlanDetails'][0]['item']['name']
# # print strmsg['PlanDetails'][0]['unit']['short_name']
# # print strmsg['PlanDetails'][0]['quantity']
# #
# # print strmsg['PlanDetails'][1]['item']['name']
# # print strmsg['PlanDetails'][1]['unit']['short_name']
# # print strmsg['PlanDetails'][1]['quantity']
# #
# # print strmsg['PlanDetails'][2]['item']['name']
# # print strmsg['PlanDetails'][2]['unit']['short_name']
# # print strmsg['PlanDetails'][2]['quantity']
#
# for plan_items in strmsg['PlanDetails']:
#     plandets = str(plan_items['quantity']) + ' ' + str(plan_items['unit']['symbol']) + ' ' + str(plan_items['item']['name'])
#     if str(plan_items['item']['name']) == "Storage":
#         storageValue = plan_items['quantity']
#     elif str(plan_items['item']['name']) == "vCPU":
#         cpuValue = plan_items['quantity']
#     elif str(plan_items['item']['name']) == "RAM":
#         memoryValue = plan_items['quantity']
#
#
#
# print storageValue
# print cpuValue
# print memoryValue
#
# PlanData = {'Flavor': 'm1.tiny', 'Image': 'TestVM', 'Zone': 'nova-ruh-highend-zone',
#             'instances': '1', 'cores': cpuValue, 'ram': int(memoryValue) * 1024, 'floating_ips': '1'}
#
# message = {'Status': True, 'ItemDetails': PlanData}
#
# print message
#
#
# import daemon
# with daemon.DaemonContext:
#
#
# Quota ={'Status': True, 'QuotaDetails': <QuotaSet cores=4, fixed_ips=-1, floating_ips=100, injected_file_content_bytes=10240, injected_file_path_bytes=255, injected_files=5, instances=1, key_pairs=10, metadata_items=1024, ram=1024, security_group_rules=20, security_groups=10, server_group_members=10, server_groups=10>}
#
# print dir(Quota['QuotaDetails'])
# network = {'Status': True, 'QuotaDetails': {u'quota': {u'subnet': 1, u'network': 1, u'floatingip': 1, u'security_group_rule': 3, u'security_group': 1, u'router': 1, u'port': 3}}}
#
# print network['QuotaDetails']['quota']['subnet']
# print network['quota']['network']
# print network['quota']['floatingip']
# print network['quota']['security_group_rule']
# print network['quota']['security_group']
# print network['quota']['router']
# print network['quota']['port']


strmsg = {
    u'service': {
        u'metadata': {

        },
        u'id': 17,
        u'name': u'InfrastructureasaService'
    },
    u'type': u'subscription.user.added',
    u'created_at': u'2015-09-16T09: 41: 43.869930Z',
    u'data': {
        u'admin': False,
        u'user': 85,
        u'id': 562,
        u'subscription': 230
    },
    u'id': u'23e3b29c-5c57-11e5-a398-fa163e6cad1a',
    u'api_version': u'1.0.0'
}

print strmsg['type']