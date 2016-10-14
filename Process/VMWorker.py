__author__ = 'OmerMahgoub'
#!/usr/bin/env python
import time
import ast
import random

import pika

from common.VM import OpenStackAdapterVMInstance
from settings import settings
from Logger import VMLogger


objSettings = settings.StackSettings()

# The below settings are coming from settings/setting.py which in return getting all the configurations from config.yml file
# Start of Settings Configuration

stackSettings = objSettings.ServiceSettings("OpenStack")
queueHostSettings = objSettings.ServiceSettings("rabbitMQ")
queueSettings = objSettings.ServiceSettings("QueueSettings")
objLogs = VMLogger()

# End of Settings Configuration

# Connection Initialization for RabbitMQ Server
count = queueSettings['retryCount']
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=queueHostSettings["host"]))
channel = connection.channel()

# User Queue Declaration
channel.queue_declare(queue=queueSettings['VMQueueName'], durable=True)

print ' [*] Waiting for messages. To exit press CTRL+C'
objLogs.Logger("VM Worker", 'info', '[*] Waiting for messages. To exit press CTRL+C')

# Send_To_VM_Queue is a Method which accepts the msg from User Queue and throws the Message to VM Queue
def Notification_Queue(UserMsg):

    # vm_queue = queueSettings['VMQueueName']  # queue name
    # connection = pika.BlockingConnection(pika.ConnectionParameters(queueHostSettings["host"]))
    # channel = connection.channel()
    # channel.queue_declare(queue=vm_queue, durable=True)  # durable=True - makes queue persistent
    #
    # headers = {  # example how headers can be used
    #              'retry_count': 1
    #              }
    # channel.basic_publish(
    #     exchange='',
    #     routing_key=vm_queue,
    #     body=UserMsg,  # must be string
    #     properties=pika.BasicProperties(
    #         delivery_mode=2,  # makes persistent job
    #         priority=0,  # default priority
    #         # timestamp=timestamp, # timestamp of job creation
    #         # expiration=str(expire), # job expiration (milliseconds from now), must be string, handled by rabbitmq
    #         headers=headers
    #     ))
    # print "[>] Message Sent to VM Queue %r" % UserMsg
    #
    # connection.close()
    pass

# The callback method is to iterate the message in the Queue. It will keep on checking for new messages
def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    objLogs.Logger("VM Worker", 'info', " [x] Received %r" % (body,))
    time.sleep(5)


    ################################OpenStack User Creation Queue #########################################
    # This program will pick the message from the User Queue and calls the OpenStack User Creation Process and waits for the Result.
    # If the User process creation is successfull it returns "True" Else "False" and for all the "False"
    # Once the Message is True, Just remove the Message from the current User Queue and throw it back to the VM Queue.
    # Once the Message is False, Just Iterate the Message in the User Queue for "n" of Times and then Save the message to the Database

    # Calling the OpenStack User Create Function

    # Split the body into seperate items
    #{'CustomerName': CustomerName, 'UserName':UserName, 'flavorName': flavor, 'EventId': EventId, 'ImageName': OSType, 'TenantId':TenantId}
    #{'EventId': id, 'CustomerId': CustomerId, 'CustomerName': CustomerName,
    # 'UserName': Admin_User_Names, 'PlanName':PlanName, 'PlanDetails':PlanDetails, 'OSType':OSType, 'AppType':'VM','FlavorName': flavorname,'app_id':app_id, 'jsondump': str(message)}
    strMessage = ast.literal_eval(body)


    EventId = strMessage['EventId']
    #CustomerName = strMessage['CustomerName']stc-demo
    CustomerName = 'stc-demo'
    UserName = 'stc'
    imageName = strMessage['OSType']
    FlavorName = strMessage['FlavorName']
    #imageName = strMessage['ImageName']
    TenantId = '56b07d1584ed4addb1b2956dcf3cb987'

    print "Printing Customername %s" % CustomerName
    print "Username %s" %UserName
    print "FlavorName %s" %FlavorName
    print "EventId %s" %EventId
    print "ImageName %s" %imageName
    print "TenantId %s" %TenantId
    exit()

    objStack = OpenStackAdapterVMInstance()
    msg = objStack.VMQueue(CustomerName, UserName, "stc_VM_" + str(random.randrange(0, 10, 1)), imageName, FlavorName, EventId, TenantId)
    #msg = {'Status': True}

    print "VM Creation/Updation Status (True/False) %s" % msg
    objLogs.Logger("VM Worker", 'info', "VM Creation/Updation Status (True/False) %s" % msg)

    ################################ End of OpenStack Project Create Function #########################################


    ############################ For Testing Purpose #####################
    # The variable msg is returned with "True" or "False', here it was hardcorded for just testing.
    # msg = "False"
    ############################ End of Testing #####################
    # First Get the Retry Times from the First Message
    print "Retry Count: %s" % properties.headers["retry_count"]
    objLogs.Logger("VM Worker", 'info', "Retry Count: %s" % properties.headers["retry_count"])

    if properties.headers["retry_count"] > count:
        print("Saving in DB")
        objLogs.Logger("VM Worker", 'info', "Saving in DB")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        try:
            if msg['Status'] == False or msg['Status'] == "Error":
                raise Exception("VM can't be created due to some reasons.Re-Queuing the Message again")
            else:
                ch.basic_ack(delivery_tag=method.delivery_tag)
                print "Successfully Operated and removed from Queue"
                objLogs.Logger("VM Worker", 'info', "Successfully Operated and removed from Queue")
                # Throw the Project Creation Message to User Queue
                Notification_Queue(body)
                # End of Throwing Message to Project Queue
        except:
            print "Just Reached Exception Area"
            objLogs.Logger("VM Worker", 'info', "Just Reached Exception Area")
            print "Before setting header, Count was %s" % properties.headers["retry_count"]
            objLogs.Logger("VM Worker", 'info', "Before setting header, Count was %s" % properties.headers["retry_count"])

            # Setting the Header and incrementing to 1
            headers = {  # example how headers can be used
                         'retry_count': properties.headers["retry_count"] + 1
                         }

            # Creating the message in the Queue Again
            channel.basic_publish(
                exchange='',
                routing_key=queueSettings['VMQueueName'],
                body=body,  # must be string
                properties=pika.BasicProperties(
                    delivery_mode=2,  # makes persistent job
                    priority=0,  # default priority
                    # timestamp=timestamp, # timestamp of job creation
                    # expiration=str(expire), # job expiration (milliseconds from now), must be string, handled by rabbitmq
                    headers=headers
                ))
            # Acknowledges that the Message is success and then through back the message to Queue.
            channel.basic_ack(delivery_tag=method.delivery_tag)

            print "Queue Acknowledged and removed"
            objLogs.Logger("VM Worker", 'info', "Queue Acknowledged and removed")
            print "[++++++Done+++++]"
            objLogs.Logger("VM Worker", 'info', "[++++++Done+++++]")
            print


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queueSettings['VMQueueName'])

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming();

connection.close()