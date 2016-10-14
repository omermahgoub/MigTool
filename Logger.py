__author__ = 'OmerMahgoub'
#!/usr/bin/env python
import sys
from oslo.config import cfg
from openstack.common import log
LOG = log.getLogger(__name__)

CONF = cfg.CONF
CONF(sys.argv[1:], project='opadapter',
     version='1.0')
log.setup('opadapter')

class VMLogger(object):

    def Logger(self, moduleName, logtype, Msg):
        # logger = logging.getLogger(__name__)
        # logger = logging.getLogger(moduleName)
        # logger.setLevel(logging.INFO)
        # # create a file handler
        #
        # handler = logging.FileHandler('VMLogs.log')
        # handler.setLevel(logging.INFO)
        #
        # # create a logging format
        #
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # handler.setFormatter(formatter)
        #
        # # add the handlers to the logger
        #
        # logger.addHandler(handler)


        if logtype == "debug":
            LOG.debug(Msg)
        elif logtype == "info":
            LOG.info(Msg)
        elif logtype == "warning":
            LOG.warn(Msg)
        elif logtype == "critical":
            LOG.critical(Msg)



