__author__ = 'OmerMahgoub'
#!/usr/bin/env python
from settings import settings

class OpenStackAdapterAuth(object):
    """ Global Parameter Declaration Window """

    objSettings = settings.StackSettings()
    cfgSettings = objSettings.ServiceSettings("OpenStack")
    usercfgSettings = objSettings.ServiceSettings("UserSettings")

    _cfgHostName = cfgSettings["host"]
    _cfgUserId = cfgSettings["user"]
    _cfgStackPwd = cfgSettings["passwd"]
    _cfgTenantName = cfgSettings["tenantName"]
    _cfgDefaultPasswd = usercfgSettings["DefaultUserPassword"]


    """ End of Global Parameter Declaration Window """

    def get_credentials(self,service,projectname):
        """Returns a creds dictionary filled with the following keys:

        * username
        * password (depending on the service)
        * project_id (depending on the service)
        * auth_url

        :param service: a string indicating the name of the service
                        requesting the credentials.
        """
        try:
            if service.lower() in ("keystone", "neutron"):
                creds = {'auth_url': '', 'username': '', 'password': '', 'tenant_name': ''};
                creds['auth_url'] = self._cfgHostName
                creds['username'] = self._cfgUserId
                creds['password'] = self._cfgStackPwd
                creds['tenant_name'] = projectname
                return creds
            elif service.lower() in ("nova", "cinder"):
                creds = {'username': '', 'api_key': '', 'auth_url': '', 'project_id': ''};
                creds['username'] = self._cfgUserId
                creds['api_key'] = self._cfgStackPwd
                creds['auth_url'] = self._cfgHostName
                creds['project_id'] = projectname
                return creds
        except Exception,e:
            return e.args

    def get_nova_neutron_credentials(self,service, UserName, TenantName):
        """Returns a creds dictionary filled with the following keys:

        * username
        * password (depending on the service)
        * project_id (depending on the service)
        * auth_url

        :param service: a string indicating the name of the service
                        requesting the credentials.
        """
        try:
            if service.lower() in ("neutron"):
                creds = {'auth_url': '', 'username': '', 'password': '', 'tenant_name': ''};
                creds['auth_url'] = self._cfgHostName
                creds['username'] = UserName
                creds['password'] = self._cfgDefaultPasswd
                creds['tenant_name'] = TenantName
                return creds
            elif service.lower() in ("nova"):
                creds = {'username': '', 'api_key': '', 'auth_url': '', 'project_id': ''};
                creds['username'] = UserName
                creds['api_key'] = self._cfgDefaultPasswd
                creds['auth_url'] = self._cfgHostName
                creds['project_id'] = TenantName
                return creds
        except Exception,e:
            return e.args



