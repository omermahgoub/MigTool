__author__ = 'OmerMahgoub'
#!/usr/bin/env python
import os
import yaml

class StackSettings:

    def ServiceSettings(self,ServiceName):
        basepath = os.path.dirname(__file__)
        keypairs = os.path.abspath(os.path.join(basepath, "config.yml"))

        with open(keypairs,'r') as f:
            doc = yaml.load(f)

        cfgServiceSettings = doc[ServiceName]
        return cfgServiceSettings

