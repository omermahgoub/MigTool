import mysql.connector

class AdapterDBOperations:

    _cnx = mysql.connector.connect(user='root', password='Adapter@321',
                              host='86.60.0.50',
                              database='OpenStackAdapter')
    def Create_Order_Requests(self,EventId, Status, ServerId):
        try:
           cursor = AdapterDBOperations._cnx.cursor()
           # cursor.execute("""
           #    select *  from service_requests
           add_service_request = ("INSERT INTO OrderStatus "
                       "(EventId, Status, ServerId) "
                       "VALUES (%s, %s, %s)")


            # Insert new Service Request
           # EventId, EventType, Service_Id, API_Version, admin_user, CustomerId, CustomerName, PlanId, PlanName, PlanDetails
           request_data = (EventId, Status, ServerId)
           cursor.execute(add_service_request, request_data)
           AdapterDBOperations._cnx.commit()
           cursor.close()
           AdapterDBOperations._cnx.close()
        except Exception,e:
            print e.args