from operator import itemgetter

import novaclient.v2.client as nvclient
import keystoneclient.v2_0.client as ksclient
import neutronclient.v2_0.client as neclient
import cinderclient.v2.client as ciclient

from common.Auth import OpenStackAdapterAuth as OpenStackAuth
from common.ProjectDB import *
import Logger
from Logger import LOG
LOG = log.getLogger(__name__)


class OpenStackAdapterProjects(object):
    objAuth = OpenStackAuth()
    kcreds = objAuth.get_credentials("keystone", "admin")
    ncreds = objAuth.get_credentials("nova", "admin")
    ccreds = objAuth.get_credentials("cinder","admin")

    _objkeystone = ksclient.Client(**kcreds)
    _objnova = nvclient.Client(**ncreds)
    _objneutron = neclient.Client(**kcreds)
    _objcinder = ciclient.Client(**ccreds)
    _objProjectDB = ProjectDB()

    _objLogs = VMLogger()
    _objLogs.Logger("Project_Availability", 'critical', "Test from Zubair")
    """ Project Stuff Starts Here """

    def Project_Availability(self, CustomerID):
        """
        :param ProjectName: a string indicating the name of the Project
                        requesting the Project Availability.
        """
        try:
            print CustomerID
            result = self._objProjectDB.Customer_Check(CustomerID)
            #print "Project Availability Function %s" % result
            if(result):
                message = {'Status': True}
                return message
            else:
                message = {'Status': False}
                return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': str(e)}
            self._objLogs.Logger("Project_Availability", 'critical', message)
            return message

    def CreateProject(self, CustomerId, CustomerName):
        try:
            resultCreation = self._objkeystone.tenants.create(CustomerName, description=None, enabled=True)
            cust_tenantId = getattr(resultCreation, 'id')

            # Store the Customer Information along with Project ID
            result = self._objProjectDB.Create_Customer_Info(CustomerId, CustomerName, cust_tenantId)
            message = {'Status': True, 'TenantId': cust_tenantId}
            return message
        except Exception, e:
            message = {'Status': 'Error', 'Type': type(e).__name__, 'Message': str(e)}
            errMsg = "Tenant Name: %s and Error is %s " % (CustomerName, message)
            self._objLogs.Logger("CreateProject", 'critical', errMsg)
            return message

    """ Project Queue Starts Here """
    #EventId, CustomerId, CustomerName, UserName, email, planname, planDetails, OSType
    def CreateProjectQueue(self, EventId, CustomerId, CustomerName, UserName, Email, PlanName, PlanDetails, extrafields):
        try:
            """"Initialization of Connection """""
            self._objLogs.Logger("CreateProjectQueue", "info", "Create Project Started")
            # Check Project Availability
            print "Creating / Updating of Project Started:"
            chk_avail = self.Project_Availability(CustomerId)

            if chk_avail['Status'] != 'Error':
                print "Is the Project Existing? %s" % chk_avail
                if chk_avail['Status'] == True:
                    strCustomerInfo = self._objProjectDB.GetTenantIdByCustomerId(CustomerId)
                    message = {'Status': True, 'TenantId':strCustomerInfo['TenantId']}
                    return message
                elif chk_avail['Status'] == False:
                    # New Customer
                    # Create New Project
                    print("Creating New Project and Assigning the New Quota")
                    # Project Creation
                    strProjectCreation = self.CreateProject(CustomerId, CustomerName)
                    print "Project Creation Status %s", strProjectCreation
                    if strProjectCreation['Status'] not in ('Error', False):
                        # Get the Plan Details
                        message = {'Status': True, 'TenantId':strProjectCreation['TenantId']}
                    else:
                        message = {'Status': False}
                    return message
            else:
                template = "An exception of type {0} occurred. Details are:\n{1!r}. Parameters are:\n{2!r}"
                message = template.format(chk_avail['Type'], chk_avail['Message'], CustomerName)
                self._objLogs.Logger("CreateProjectQueue", "critical", message)
                return {'Status': 'Error'}
        except Exception, e:
            template = "An exception of type {0} occurred. Details are:\n{1!r}."
            message = template.format(type(e).__name__, e.args)
            self._objLogs.Logger("CreateProjectQueue", "critical", str(e))
            return {'Status': 'Error'}

    """ Project Queue Ends Here """


