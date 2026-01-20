import cfe_framework.utils as utils
import xml.etree.ElementTree as ET
from .metadataobject import MetaDataObject
from enum import Enum

class ReturnValuesReuse(Enum):

    DontUse = "DontUse"
    DuringRequest = "DuringRequest"
    DuringSession = "DuringSession"

class CommonModule(MetaDataObject):

    def __init__(self, name, synonym = None, id=None):
        super().__init__(name, synonym, id)

        self.Global                     = None
        self.ClientManagedApplication   = None
        self.ExternalConnection         = None
        self.ClientOrdinaryApplication  = None
        self.ServerCall                 = None
        self.Server                     = None
        self.Privileged                 = None
        
        self.ReturnValuesReuse = ReturnValuesReuse.DontUse

        self.ModuleText = None

    def serialize(self, outputDirectory):

        text = self.buildXMLCommonModule()
        
        targetFile = f'CommonModules/{self.Name}.xml'
        utils.saveText(text, outputDirectory, targetFile)

        if self.ModuleText != None:

            targetFile = f'CommonModules/{self.Name}/Ext/module.bsl'
            utils.saveText(self.ModuleText.encode('utf-8'), outputDirectory, targetFile)

        pass

    def buildXMLCommonModule(self):

        metaDataObjectNode = ET.Element("MetaDataObject")

        propertiesNode = ET.Element("Properties")
        self.generateCommonProperties(propertiesNode)

        flags = ["Global", 
                 "ClientManagedApplication",
                 "Server",
                 "ExternalConnection",
                 "ClientOrdinaryApplication",
                 "ServerCall",
                 "Privileged"]

        for flag in flags:
            
            attrVal = getattr(self, flag)
            
            if attrVal:
                propertiesNode.append(utils.makeTextNode(flag, utils.booleanToString()))

        propertiesNode.append(utils.makeTextNode("ReturnValuesReuse", self.ReturnValuesReuse))

        commonModuleNode = ET.Element("CommonModule")
        commonModuleNode.attrib["uuid"] = self.UUID
        commonModuleNode.append(propertiesNode)

        metaDataObjectNode.append(commonModuleNode)

        return utils.writeDocumentToString(metaDataObjectNode, True)