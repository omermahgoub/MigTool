#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.abspath("/Projects/OpenStackAdapter"))

from common.VMStatus import OpenStackAdapterVMStatus
import mysql.connector
from mysql.connector import Error
from mysql.connector import MySQLConnection
import time,threading

dbconfig = {'password': 'Adapter@321', 'host': '86.60.0.50', 'user': 'root', 'database': 'OpenStackAdapter'}

#serverId, username, tenantname
def CheckOrderStatus(ServerId, UserName, TenantName):
    objVMStatus = OpenStackAdapterVMStatus()
    status = objVMStatus.GetServerStatus(UserName, TenantName, ServerId)
    print "Printing Status %s" % status
    # # # Update the serverId in database to the latest Status
    if status['Status'] == True:
        Update_OrderStatus('Pending', ServerId)
        print ServerId + " Updated successfully";
    else:
        print "Error Status FOund"


def Update_OrderStatus(orderStatus, ServerId):
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute("UPDATE OrderStatus SET Status=%s WHERE ServerId=%s", (orderStatus, ServerId))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def MainCall():
    count = 1
    while True:
        try:
	    conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute("SELECT ServerId, admin_user, tenant_name FROM OrderStatus WHERE Status = 'InProgress'")

            row = cursor.fetchall()
            total_rows = cursor.rowcount
            cursor.close()
            conn.close()

            if total_rows >= 1:
               for serverId,username,tenantname in row:
                   print CheckOrderStatus(serverId, username, tenantname)
                   #print serverId,username,tenantname
            else:
               message = {'Status': False}
               #return message

            print("Running Script Every 5 Seconds...")
            time.sleep(5)
            if count % 120 is 0:#20 minutes
              count =1
            count += 1
        except Exception,e:
            print("Exception: %s"%str(e))

if __name__ == '__main__':
    try:
       MainCall()
    except Exception,e:
       print("Exception: %s"%str(e))
