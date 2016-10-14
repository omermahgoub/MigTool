from ceilometerclient import client
import hashlib
import csv
from os import environ as env

server_name = 'Server_name'
meter = 'cpu_util'
start_date = "2014-11-19T00:00:00"
end_date = "2014-11-19T23:00:00"

keystone = dict(os_username='admin',
                os_password='AwalNet@123',
                os_auth_url='http://172.18.112.2:5000/v2.0',
                os_tenant_name='StatsProject')

ceilometer = client.get_client(2, **keystone)


def instances(cc):
    """
    Get all instances Id in Ceilometer
    """
    inst_list = list()
    meters_list = cc.meters.list()
    [inst_list.append(meters.resource_id) for meters in meters_list if meters.name == 'instance']
    print inst_list
    return inst_list


def instance_samples(cc, inst_list):
    """
    Get instances Id running within the server
    """
    instances_server = list()
    for instance in inst_list:
        query = [dict(field='timestamp', op='gt', value=start_date),
                 dict(field='timestamp', op='lt', value=end_date),
                 dict(field='resource', op='eq', value=instance)]
        samples = cc.samples.list(meter_name='instance',
                                  q=query,
                                  limit=1)
        if samples:
            hash1 = hashlib.sha224(samples[0].project_id + server_name)
            hash1 = hash1.hexdigest()
            if hash1 == samples[0].resource_metadata['host']:
                instances_server.append(samples[0].resource_id)
    return instances_server
#
#
# def meter_samples(cc, inst_list):
#     for instance in inst_list:
#         query = [dict(field='timestamp', op='gt', value=start_date),
#                  dict(field='timestamp', op='lt', value=end_date),
#                  dict(field='resource', op='eq', value=instance)]
#         samples = cc.samples.list(meter_name=meter,
#                                   q=query)
#         samples = list(reversed(samples))
#         csv_writer(samples, instance)
#
#
# def csv_writer(data, instance):
#     """
#     Writes a CSV file
#     """
#     path = "{0}-{1}-{2}.csv".format(meter, instance, server_name)
#     with open(path, "wb") as out_file:
#         writer = csv.writer(out_file, delimiter=',')
#         #Write rows to CSV file, if there is another field required it should add here.
#         for row in data:
#             rw = list()
#             rw.append("{0}".format(row.counter_volume))
#             rw.append("{0}".format(row.timestamp))
#             rw.append("{0}".format(row.resource_metadata['vcpus']))
#             writer.writerow(rw)


instance_list = instances(ceilometer)
print instance_list
# instances = instance_samples(ceilometer, instance_list)
# meter_samples(ceilometer, instances)