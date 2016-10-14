    def CreateVM(self, CustomerName, UserName, VmName, ImageName, flavorName, network_label, EventId, TenantId):
        try:
            objAuth = Auth.OpenStackAdapterAuth()
            objNetworks = networks.OpenStackAdapterNetworks()
            novacreds = objAuth.get_nova_neutron_credentials("nova", UserName, CustomerName)
            objnova = nvclient.Client(**novacreds)

            # Create a network and one subnet
            print "Creating Private Network"
            #network = objNetworks.create_private_network(UserName, CustomerName, network_label)
            print "Printing Network %s", network
            # print network['NetworkDetails']['network']['id']

            #if network['Status'] == True:
            #    print "Creating Private Router"
                # Plug a router between our private network and an external network
                #(self, name, private_net_name, public_net_name, UserName, CustomerName):
                #("Router_7865","net_id_7865","net04_ext",'mamerpasha','MiracleSoft1')
            #    router = objNetworks.create_router("Router_Id_" + str(random.randrange(0, 8000, 3)), network_label, "net04_ext", UserName, CustomerName)

            #    print "Router Information %s" % router

            #    image = objnova.images.find(name=ImageName)
            #    flavor = objnova.flavors.find(name=flavorName)
            #    network_details = objnova.networks.find(label=network_label)

            print "Tenant ID from Queue %s" % TenantId

            #    securityRule = objNetworks.create_security_rules(UserName, CustomerName, TenantId)
            #    print "Security Rule %s" % securityRule

            #    print network_details.id

                # Creating Instance
            print "Creating Instance"
            print "Image %s" % image
            print "ImageName Parameter %s" % ImageName
            print "FlavorName from Parameter %s" % flavorName
            print "Flavor Name %s" % flavor
            print "VM Name %s" % VmName
           #    print "Key Name %s" % UserName+"_key"
           #    print "Network ID %s" % network_details.id
            instance = objnova.servers.create(name=VmName, image=image, flavor=flavor, key_name=None, nics=[{'net-id': '81a1ba70-7303-4763-b791-9ed50a58cff8'}])
                #instance = objnova.servers.create(name=VmName, image=image,
                #                               flavor=flavor, key_name=None)


            message = {'Status': True, 'ServerId': instance.id}
                #self.Create_Order(EventId, 'Pending',instance.id)
                #Create_Order(self, EventId, Status, ServerId, admin_user, tenant_name, app_type):
             self._objProjectDB.Create_Order(EventId, 'InProgress', instance.id, UserName, CustomerName, 'VM')

             return message
            else:
                message = {'Status': False}
                return message
