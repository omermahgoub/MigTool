__author__ = 'OmerMahgoub'
import mysql.connector
from mysql.connector import Error
from mysql.connector import MySQLConnection



class ProjectDB:
    def Customer_Check(self, CustomerId):
        try:
            dbconfig = {'password': 'Adapter@321', 'host': '86.60.0.50', 'user': 'root', 'database': 'OpenStackAdapter'}
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM CustomerInfo WHERE Customer_ID =(%s)' % (CustomerId,))

            row = cursor.fetchone()
            rowc = cursor.rowcount

            if rowc >= 1:
                return True
            else:
                return False

            cursor.close()
            conn.close()
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def GetTenantIdByCustomerId(self, CustomerId):
        try:
            dbconfig = {'password': 'Adapter@321', 'host': '86.60.0.50', 'user': 'root', 'database': 'OpenStackAdapter'}
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute('SELECT TenantId FROM CustomerInfo WHERE Customer_ID =(%s)' % (CustomerId,))

            row = cursor.fetchone()
            rowc = cursor.rowcount

            if rowc >= 1:
                message = {'Status': True, 'TenantId': row[0]}
                return message
            else:
                message = {'Status': False}
                return message
            cursor.close()
            conn.close()
        except Error as e:
             message = {'Status': 'Error'}
        finally:
            cursor.close()
            conn.close()

    def Create_Customer_Info(self, CustomerId, CustomerName, TenantId):
        query = "INSERT INTO CustomerInfo(Customer_ID, CustomerName, TenantId) " \
                "VALUES(%s,%s,%s)"
        args = (CustomerId, CustomerName, TenantId)

        try:
            db_config = {'password': 'Adapter@321', 'host': '86.60.0.50', 'user': 'root', 'database': 'OpenStackAdapter'}
            conn = MySQLConnection(**db_config)

            cursor = conn.cursor()
            cursor.execute(query, args)
            conn.commit()
        except Error as error:
            print(error)

        finally:
            cursor.close()
            conn.close()

    def Delete_CustomerInfo(self, CustomerId):
        try:
            dbconfig = {'password': 'Adapter@321', 'host': '86.60.0.50', 'user': 'root', 'database': 'OpenStackAdapter'}
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM CustomerInfo WHERE Customer_ID =(%s)' % (CustomerId,))

            conn.commit()
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def Create_Order(self, EventId, Status, ServerId, admin_user, tenant_name, app_type):
        query = "INSERT INTO OrderStatus(EventId, Status, ServerId, admin_user, tenant_name, app_type, created) " \
                "VALUES(%s,%s,%s,%s,%s,%s,NOW())"
        args = (EventId, Status, ServerId, admin_user, tenant_name, app_type)
        try:
            db_config = {'password': 'Adapter@321', 'host': '86.60.0.50', 'user': 'root', 'database': 'OpenStackAdapter'}
            conn = MySQLConnection(**db_config)

            cursor = conn.cursor()
            cursor.execute(query, args)
            conn.commit()
        except Error as error:
            print(error)
        finally:
            cursor.close()
            conn.close()

