# __author__ = 'OmerMahgoub'
# #!/usr/bin/env python
# import pika
#
# # Add the order to the STCSTACK Queue
# connection = pika.BlockingConnection(pika.ConnectionParameters(
#     host='localhost'))
# channel = connection.channel()
#
# channel.queue_declare(queue='Project_Queue', durable=True)
#
message = {
    "id": "e786786",
    "type": "subscription.created",
    "service_id": 3,
    "created_at": "2015-07-02T00:00:00.000Z",
    "data": {
        "Subscription": {
            "id": "1",
            "customer": {
                "id": "21321231231321",
                "name": "Mohammad Zubair3 Pasha"
            },
            "price": {
                "id": "1",
                "type": "one_time",
                "period": 1,
                "period_unit": "month",
                "amount": 78666.5,
                "currency": "SAR",
                "created": "2015-02-01T00:00:00.000Z",
                "modified": "2015-02-01T00:00:00.000Z"
            },
            "admin_user": "12456",
            "status": "pending",
            "start": "2015-02-01T00:00:00.000Z",
            "canceled_at": "2015-02-01T00:00:00.000Z",
            "cancel_reason": "customer_request",
            "created": "2015-02-01T00:00:00.000Z",
            "Plan": {
                "id": "1",
                "name": "Premium",
                "initial_price": {
                    "price": {
                        "id": "1",
                        "type": "one_time",
                        "period": 1,
                        "period_unit": "month",
                        "amount": 78666.5,
                        "currency": "SAR",
                        "created": "2015-02-01T00:00:00.000Z",
                        "modified": "2015-02-01T00:00:00.000Z"
                    }
                },
                "description": "Premium Plan",
                "created": "2015-07-01T00:00:00.000Z",
                "modified": "2015-07-01T00:00:00.000Z",
                "plan_items": [
                    {
                        "id": 1,
                        "item": {
                            "itemid": 1,
                            "meta_data": "metadata",
                            "name": "Storage",
                            "description": "Storage for this plan\"",
                            "created": "2015-07-02T00:00:00.000Z",
                            "modified": "2015-07-02T00:00:00.000Z"
                        },
                        "unit": {
                            "id": 1,
                            "name": "GigaByte",
                            "short_name": "GB",
                            "symbol": "GB"
                        },
                        "quantity": "4.0"
                    },
                    {
                        "id": 2,
                        "item": {
                            "itemid": 1,
                            "meta_data": "metadata",
                            "name": "RAM",
                            "description": "Memory for this plan",
                            "created": "2015-07-02T00:00:00.000Z",
                            "modified": "2015-07-02T00:00:00.000Z"
                        },
                        "unit": {
                            "id": 1,
                            "name": "GigaByte",
                            "short_name": "GB",
                            "symbol": "GB"
                        },
                        "quantity": "1"
                    },
                    {
                        "id": 3,
                        "item": {
                            "itemid": 3,
                            "meta_data": "metadata",
                            "name": "vCPU",
                            "description": "Memory for this plan",
                            "created": "2015-07-02T00:00:00.000Z",
                            "modified": "2015-07-02T00:00:00.000Z"
                        },
                        "unit": {
                            "id": 1,
                            "name": "",
                            "short_name": "",
                            "symbol": ""
                        },
                        "quantity": "4"
                    }
                ]
            }
        }
    },
    "api_version": "1"
}
# # EventId = message['id']
# # EventType = message['type']
# # Service_Id = message['service_id']
# # API_Version = message['api_version']
# # Admin_User = message['data']['Subscription']['admin_user']
# # CustomerId = message['data']['Subscription']['customer']['id']
# # CustomerName = message['data']['Subscription']['customer']['name']
# # PlanId = message['data']['Subscription']['Plan']['id']
# # PlanName = message['data']['Subscription']['Plan']['name']
# # PlanDescription = message['data']['Subscription']['Plan']['description']
# # PlanDetails = message['data']['Subscription']['Plan']['plan_items']
#
# strMessage = {'EventId': u'3856fea0-262e-11e5-ab1a-fa163ece429e', 'PlanName': u'Basic Plan', 'PlanDetails': [{u'item': {u'description': u'Memory for this plan', u'created': u'2015-07-07T11:58:16.024160Z', u'modified': u'2015-07-07T11:58:16.026230Z', u'units': [{u'symbol': u'', u'id': u'gigabyte', u'short_name': u'GB', u'name': u'GigaByte'}], u'id': 6, u'name': u'RAM'}, u'id': 6, u'unit': {u'symbol': u'', u'id': u'gigabyte', u'short_name': u'GB', u'name': u'GigaByte'}, u'quantity': u'4.0'}, {u'item': {u'description': u'Virtual CPU for this plan', u'created': u'2015-07-07T11:59:05.118344Z', u'modified': u'2015-07-07T11:59:05.119085Z', u'units': [], u'id': 7, u'name': u'vCPU'}, u'id': 5, u'unit': None, u'quantity': u'4.0'}, {u'item': {u'description': u'Storage for this plan', u'created': u'2015-07-07T11:58:01.635776Z', u'modified': u'2015-07-07T11:58:01.638027Z', u'units': [{u'symbol': u'', u'id': u'gigabyte', u'short_name': u'GB', u'name': u'GigaByte'}], u'id': 5, u'name': u'Storage'}, u'id': 4, u'unit': {u'symbol': u'', u'id': u'gigabyte', u'short_name': u'GB', u'name': u'GigaByte'}, u'quantity': u'10.0'}], 'CustomerName': u'Sulaiman Alfaifi', 'ExtraFields': u'Centos-7'}
# """End of Parsing the request object and saving it to the database """
#
# """Save the details to the database"""
# # objStackDb = StackDB()
# # objStackDb.Create_Service_Requests(EventId, EventType, Service_Id, API_Version, Admin_User, CustomerId, CustomerName, PlanId, PlanName, str(PlanDetails))
#
# """ Body for Project Queue """
# #projectDetails = {'EventId': EventId,'CustomerName': CustomerName,'PlanName':PlanName,'PlanDetails':PlanDetails}
#
# headers = { # example how headers can be used
# 'retry_count': 1
# }
# channel.basic_publish(exchange='',
#     routing_key='Project_Queue',
#     body=str(strMessage),
#     properties=pika.BasicProperties(
#         delivery_mode=2, # makes persistent job
#         priority=0, # default priority
#         headers=headers
#     ))
# connection.close()
message = {'EventId': u'751334e4-2633-11e5-ab1a-fa163ece429e', 'PlanName': u'Basic Plan', 'PlanDetails': [{u'item': {u'description': u'Memory for this plan', u'created': u'2015-07-07T11:58:16.024160Z', u'modified': u'2015-07-07T11:58:16.026230Z', u'units': [{u'symbol': u'', u'id': u'gigabyte', u'short_name': u'GB', u'name': u'GigaByte'}], u'id': 6, u'name': u'RAM'}, u'id': 6, u'unit': {u'symbol': u'', u'id': u'gigabyte', u'short_name': u'GB', u'name': u'GigaByte'}, u'quantity': u'4.0'}, {u'item': {u'description': u'Virtual CPU for this plan', u'created': u'2015-07-07T11:59:05.118344Z', u'modified': u'2015-07-07T11:59:05.119085Z', u'units': [], u'id': 7, u'name': u'vCPU'}, u'id': 5, u'unit': None, u'quantity': u'4.0'}, {u'item': {u'description': u'Storage for this plan', u'created': u'2015-07-07T11:58:01.635776Z', u'modified': u'2015-07-07T11:58:01.638027Z', u'units': [{u'symbol': u'', u'id': u'gigabyte', u'short_name': u'GB', u'name': u'GigaByte'}], u'id': 5, u'name': u'Storage'}, u'id': 4, u'unit': {u'symbol': u'', u'id': u'gigabyte', u'short_name': u'GB', u'name': u'GigaByte'}, u'quantity': u'10.0'}], 'OSType': u'Centos-7', 'CustomerName': u'Sulaiman Alfaifi'}
for plan_items in message['PlanDetails']:
    if str(plan_items['item']['name']) == "Storage":
        storageValue = float(plan_items['quantity'])
    elif str(plan_items['item']['name']) == "vCPU":
        cpuValue = float(plan_items['quantity'])
    elif str(plan_items['item']['name']) == "RAM":
        memoryValue = float(plan_items['quantity'])

print int(storageValue)
print int(cpuValue)
print int(memoryValue)
print int(memoryValue)
print message['OSType']

