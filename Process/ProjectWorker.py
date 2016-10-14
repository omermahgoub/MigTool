__author__ = 'OmerMahgoub'

#!/usr/bin/env python
import time, sys
import ast

import pika

# from OpenStackFunctions import OpenStackFunctions
from common.Projects import OpenStackAdapterProjects
from settings import settings

import Logger
from Logger import LOG
objSettings = settings.StackSettings()

# The below settings are coming from settings/setting.py which in return getting all the configurations from config.yml file
# Start of Settings Configuration

stackSettings = objSettings.ServiceSettings("OpenStack")
queueHostSettings = objSettings.ServiceSettings("rabbitMQ")
queueSettings = objSettings.ServiceSettings("QueueSettings")

objStack = OpenStackAdapterProjects()



# End of Settings Configuration

# Connection Initialization for RabbitMQ Server
count = queueSettings['retryCount']
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=queueHostSettings["host"]))
channel = connection.channel()

# Project Queue Declaration
channel.queue_declare(queue=queueSettings['ProjectQueueName'], durable=True)

print ' [*] Waiting for messages. To exit press CTRL+C'
#Logger(self,moduleName,type,Msg):
LOG.info("Project Worker [*] Waiting for messages. To exit press CTRL+C")

# Send_To_User_Queue is a Method which accepts the msg from Project Queue and throws the Message to User Queue

def Send_To_User_Queue(UserMsg):
    ##print UserMsg
    user_queue = queueSettings['UserQueueName']  # queue name

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
    LOG.info("Project Worker -- [>] Message Sent to User Queue Successfully")

    connection.close()

# The callback method is to iterate the message in the Queue. It will keep on checking for new messages
def callback(ch, method, properties, body):
    LOG.info("Project Worker -- Received Request")
    time.sleep(5)

    ################################OpenStack Project Creation Queue #########################################
    # This program will pick the message from the Project Queue and calls the OpenStack Project Creation Process and waits for the Result.
    # If the project process creation is successfull it returns "True" Else "False" and for all the "False"
    # Once the Message is True, Just remove the Message from the current Project Queue and throw it back to the User Queue.
    # Once the Message is False, Just Iterate the Message in the Project Queue for "n" of Times and then Save the message to the Database

    # Calling the OpenStack Project Create Function

    # Split the body into seperate items
    strMessage = ast.literal_eval(body)
    EventId = strMessage['EventId']
    CustomerId = strMessage['CustomerId']
    CustomerName = strMessage['CustomerName']
    UserName = strMessage['UserName']
    email = None
    planname = strMessage['PlanName']
    planDetails = strMessage['PlanDetails']
    projectname = strMessage['CustomerName']
    OSType = strMessage['OSType']
    AppType = strMessage['AppType']
    FlavorName = strMessage['FlavorName']
    app_id = strMessage['app_id']

    msg = objStack.CreateProjectQueue(EventId, CustomerId, CustomerName, UserName, email, planname, planDetails, OSType)
    LOG.info("Project Worker %s"% msg)

    LOG.info("Project Worker -- Project Creation/Updation Status (True/False) %s" % msg['Status'])

    ################################ End of OpenStack Project Create Function #########################################


    ################################ For Testing Purpose ##################################################################
    # The variable msg is returned with "True" or "False', here it was hardcoded for just testing.
    # msg = "False"
    ############################ End of Testing #####################
    # First Get the Retry Times from the First Message

    if properties.headers["retry_count"] > count:
        LOG.info("Project Worker -- Saving in DB")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        try:
            if msg['Status'] == False or msg['Status'] == "Error":
                raise Exception("Project can't be created due to some reasons.Re-Queuing the Message again")
            else:
                ch.basic_ack(delivery_tag=method.delivery_tag)
                LOG.info("Project Worker -- Successfully Operated and removed from Queue")
                # Throw the Project Creation Message to User Queue

                UserQueueDetails = {'body':body, 'FlavorName': FlavorName, 'TenantId': msg['TenantId'], 'app_id':app_id, 'app_type':AppType}

                Send_To_User_Queue(str(UserQueueDetails))
                # End of Throwing Message to Project Queue
        except:
            LOG.info("Project Worker -- Just Reached Exception Area")
            LOG.info("Project Worker -- Before setting header, Count was %s" % properties.headers["retry_count"])

            # Setting the Header and incrementing to 1
            headers = {  # example how headers can be used
                         'retry_count': properties.headers["retry_count"] + 1
                         }

            # Creating the message in the Queue Again
            channel.basic_publish(
                exchange='',
                routing_key=queueSettings['ProjectQueueName'],
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


            LOG.info("Project Worker -- Queue Acknowledged and removed")
            LOG.info("Project Worker -- [++++++Done+++++]")

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue=queueSettings['ProjectQueueName'])

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

connection.close()

