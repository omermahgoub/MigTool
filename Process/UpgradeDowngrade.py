__author__ = 'OmerMahgoub'

#!/usr/bin/env python
import time

import pika

# from OpenStackFunctions import OpenStackFunctions
from common.Projects import OpenStackAdapterProjects
from settings import settings

objSettings = settings.StackSettings()

# The below settings are coming from settings/setting.py which in return getting all the configurations from config.yml file
# Start of Settings Configuration

stackSettings = objSettings.ServiceSettings("OpenStack")
queueHostSettings = objSettings.ServiceSettings("rabbitMQ")
queueSettings = objSettings.ServiceSettings("QueueSettings")

# End of Settings Configuration

# Connection Initialization for RabbitMQ Server
count = queueSettings['retryCount']
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=queueHostSettings["host"]))
channel = connection.channel()

# Project Queue Declaration
channel.queue_declare(queue=queueSettings['UpgradeQueueName'], durable=True)

print ' [*] Waiting for messages. To exit press CTRL+C'

# Send_To_User_Queue is a Method which accepts the msg from Project Queue and throws the Message to User Queue
def Send_To_Resize_Queue(UserMsg):
    user_queue = queueSettings['ResizeQueueName']  # queue name

    connection = pika.BlockingConnection(pika.ConnectionParameters(queueHostSettings["host"]))
    channel = connection.channel()
    channel.queue_declare(queue=user_queue, durable=True)  # durable=True - makes queue persistent

    # message = "Mohammad Zubair Pasha"
    headers = {  # example how headers can be used
                 'retry_count': 1
                 }
    channel.basic_publish(
        exchange='',
        routing_key=user_queue,
        body=UserMsg,  # must be string
        properties=pika.BasicProperties(
            delivery_mode=2,  # makes persistent job
            priority=0,  # default priority
            # timestamp=timestamp, # timestamp of job creation
            # expiration=str(expire), # job expiration (milliseconds from now), must be string, handled by rabbitmq
            headers=headers
        ))
    print "[>] Message Sent to User Queue %r" % UserMsg

    connection.close()

# The callback method is to iterate the message in the Queue. It will keep on checking for new messages
def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    time.sleep(5)
    # Split the body into seperate items
    itemsList = body.split(",")

    orderId = itemsList[0]
    userid = itemsList[1]
    email = itemsList[2]
    planname = itemsList[3]
    projectname = itemsList[4]
    requestType = itemsList[5]
    serverId = itemsList[6]

    objStack = OpenStackAdapterProjects()

    if requestType == "upgrade":
        msg = objStack.UpgradeProjectQueue(projectname, userid, planname, serverId)
    elif requestType == "downgrade":
        msg = objStack.DowngradeProjectQueue(projectname, userid, planname, serverId)

    print "Project Downgrade/ Status (True/False) %s" % msg['Status']

    print "Retry Count: %s" % properties.headers["retry_count"]

    if properties.headers["retry_count"] > count:
        print("Saving in DB")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        try:
            if msg['Status'] == False or msg['Status'] == "Error":
                raise Exception("Project can't be created due to some reasons.Re-Queuing the Message again")
            else:
                ch.basic_ack(delivery_tag=method.delivery_tag)
                print "Successfully Operated and removed from Queue"
                # Throw the Project Creation Message to User Queue

                UserQueueDetails = {'body':body,'PlanDetails': msg["PlanDetails"]}
                Send_To_Resize_Queue(str(UserQueueDetails))
                # End of Throwing Message to Project Queue
        except:
            print "Just Reached Exception Area"
            print "Before setting header, Count was %s" % properties.headers["retry_count"]

            # Setting the Header and incrementing to 1
            headers = {  # example how headers can be used
                         'retry_count': properties.headers["retry_count"] + 1
                         }

            # Creating the message in the Queue Again
            channel.basic_publish(
                exchange='',
                routing_key=queueSettings['UpgradeQueueName'],
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
            print "[++++++Done+++++]"
            print


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queueSettings['UpgradeQueueName'])

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming();

connection.close()