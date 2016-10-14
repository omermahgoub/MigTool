__author__ = 'OmerMahgoub'

#!/usr/bin/env python
import time
import ast

import pika

# from OpenStackFunctions import OpenStackFunctions
from common.Projects import OpenStackAdapterProjects
from settings import settings
import Logger
objSettings = settings.StackSettings()

# The below settings are coming from settings/setting.py which in return getting all the configurations from config.yml file
# Start of Settings Configuration

stackSettings = objSettings.ServiceSettings("OpenStack")
queueHostSettings = objSettings.ServiceSettings("rabbitMQ")
queueSettings = objSettings.ServiceSettings("QueueSettings")

objLogs = Logger.VMLogger()


# End of Settings Configuration

# Connection Initialization for RabbitMQ Server
count = queueSettings['retryCount']
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=queueHostSettings["host"]))
channel = connection.channel()

# Project Queue Declaration
channel.queue_declare(queue=queueSettings['AddonQueueName'], durable=True)

print ' [*] Waiting for messages. To exit press CTRL+C'
#Logger(self,moduleName,type,Msg):
objLogs.Logger("Addon Worker", 'info', '[*] Waiting for messages. To exit press CTRL+C')

# Send_To_User_Queue is a Method which accepts the msg from Project Queue and throws the Message to User Queue
def Notification_Queue(UserMsg):
    #print UserMsg
    # user_queue = queueSettings['UserQueueName']  # queue name
    #
    # connection = pika.BlockingConnection(pika.ConnectionParameters(queueHostSettings["host"]))
    # channel = connection.channel()
    # channel.queue_declare(queue=user_queue, durable=True)  # durable=True - makes queue persistent
    #
    # # message = "Mohammad Zubair Pasha"
    # headers = {  # example how headers can be used
    #              'retry_count': 1
    #              }
    # channel.basic_publish(
    #     exchange='',
    #     routing_key=user_queue,
    #     body=UserMsg,  # must be string
    #     properties=pika.BasicProperties(
    #         delivery_mode=2,  # makes persistent job
    #         priority=0,  # default priority
    #         # timestamp=timestamp, # timestamp of job creation
    #         # expiration=str(expire), # job expiration (milliseconds from now), must be string, handled by rabbitmq
    #         headers=headers
    #     ))
    # print "[>] Message Sent to User Queue %r" % UserMsg
    # objLogs.Logger("Project Worker", 'info', "[>] Message Sent to User Queue %r" % UserMsg)
    #
    # connection.close()
    pass

# The callback method is to iterate the message in the Queue. It will keep on checking for new messages
def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    objLogs.Logger("Addon Worker", 'info', " [x] Received %r" % (body,))
    time.sleep(5)

    ################################OpenStack Project Creation Queue #########################################
    # This program will pick the message from the Project Queue and calls the OpenStack Project Creation Process and waits for the Result.
    # If the project process creation is successfull it returns "True" Else "False" and for all the "False"
    # Once the Message is True, Just remove the Message from the current Project Queue and throw it back to the User Queue.
    # Once the Message is False, Just Iterate the Message in the Project Queue for "n" of Times and then Save the message to the Database

    # Calling the OpenStack Project Create Function

    # Split the body into seperate items
    #{'EventId': u'6fb7eb7e-3f39-11e5-ab1a-fa163ece429e', 'UserName': u'mamer', 'CustomerName': 'Zubair_36', 'addon_type': 'FloatingIP', 'CustomerId': 36, 'quantity': 2.0}
    strMessage = ast.literal_eval(body)
    EventId = strMessage['EventId']
    CustomerId = strMessage['CustomerId']
    CustomerName = strMessage['CustomerName']
    UserName = strMessage['UserName']
    AddonType = strMessage['addon_type']
    AddonQuantity = strMessage['quantity']

    #{'EventId': u'db49e036-3f7a-11e5-ab1a-fa163ece429e', 'UserName': u'mamer', 'CustomerName': 'Zubair_36', 'addon_type': 'FloatingIP', 'CustomerId': 36, 'quantity': 2.0}
    objStack = OpenStackAdapterProjects()
    #msg = objStack.CreateAddonQueue(EventId, CustomerId, CustomerName, UserName, AddonType, AddonQuantity)
    #{'EventId': u'6fb7eb7e-3f39-11e5-ab1a-fa163ece429e', 'UserName': u'mamer', 'CustomerName': 'Zubair_36', 'addon_type': 'FloatingIP', 'CustomerId': 36, 'quantity': 2.0}
    msg = objStack.CreateAddonQueue('6fb7eb7e-3f39-11e5-ab1a-fa163ece429e',355,'MiracleSoft25','mzubair','FloatingIP',1)

    print "Result %s" % msg
    #msg = {'Status': True, 'flavorName': 'm1.tiny'}
    print msg
    objLogs.Logger("Addon Worker", 'info', msg)

    print "Addon Creation/Updation Status (True/False) %s" % msg['Status']
    objLogs.Logger("Addon Worker", 'info', "Addon Creation/Updation Status (True/False) %s" % msg['Status'])
    # print "Plan Details are as follows: %s" % msg["PlanDetails"]

    ################################ End of OpenStack Project Create Function #########################################


    ################################ For Testing Purpose ##################################################################
    # The variable msg is returned with "True" or "False', here it was hardcoded for just testing.
    # msg = "False"
    ############################ End of Testing #####################
    # First Get the Retry Times from the First Message
    print "Retry Count: %s" % properties.headers["retry_count"]
    objLogs.Logger("Addon Worker", 'info', "Retry Count: %s" % properties.headers["retry_count"])

    if properties.headers["retry_count"] > count:
        print("Saving in DB")
        objLogs.Logger("Addon Worker", 'info', "Saving in DB")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        try:
            if msg['Status'] == False or msg['Status'] == "Error":
                raise Exception("Addon can't be created due to some reasons.Re-Queuing the Message again")
            else:
                ch.basic_ack(delivery_tag=method.delivery_tag)
                print "Successfully Operated and removed from Queue"
                objLogs.Logger("Addon Worker", 'info', "Successfully Operated and removed from Queue")
                # Throw the Project Creation Message to User Queue

                NotifyQueueDetails = {''}

                Notification_Queue(str(NotifyQueueDetails))
                # End of Throwing Message to Project Queue
        except:
            print "Just Reached Exception Area"
            objLogs.Logger("Addon Worker", 'info', "Just Reached Exception Area")
            print "Before setting header, Count was %s" % properties.headers["retry_count"]
            objLogs.Logger("Addon Worker", 'info', "Before setting header, Count was %s" % properties.headers["retry_count"])

            # Setting the Header and incrementing to 1
            headers = {  # example how headers can be used
                         'retry_count': properties.headers["retry_count"] + 1
                         }

            # Creating the message in the Queue Again
            channel.basic_publish(
                exchange='',
                routing_key=queueSettings['AddonQueueName'],
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
            objLogs.Logger("Addon Worker", 'info', "Queue Acknowledged and removed")
            print "[++++++Done+++++]"
            objLogs.Logger("Addon Worker", 'info', "[++++++Done+++++]")


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queueSettings['AddonQueueName'])

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming();

connection.close()
