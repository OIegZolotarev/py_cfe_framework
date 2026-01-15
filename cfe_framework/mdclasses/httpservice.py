import xml.etree.ElementTree as ET

import cfe_framework.utils as utils
from .genericV8Object import GenericV8Object

class HTTPService(GenericV8Object):

    def __init__(self, name, synonym=None, id=None):
        super().__init__(name, synonym, id)

    def makeXMLDescriptor(self):

        metaDataObjectNode              = ET.Element("MetaDataObject")
        httpServiceNode                 = ET.Element("HTTPService")        
        httpServiceNode.attrib['uuid']  = self.UUID

        internalInfoNode = ET.Element("InternalInfo")

        self.generateInternalInfoBlock(internalInfoNode)

        propertiesNode = ET.Element("Properties")
        self.generateCommonProperties(propertiesNode)

        httpServiceNode.append(internalInfoNode)
        httpServiceNode.append(propertiesNode)

        childObjectsNode = ET.Element("ChildObjects")
        httpServiceNode.append(childObjectsNode)

        metaDataObjectNode.append(httpServiceNode)
        return utils.writeDocumentToString(metaDataObjectNode, True)
    
    def serialize(self, outputDirectory):

        descriptor = self.makeXMLDescriptor()
        descriptorFile = f'HTTPServices/{self.Name}.xml'

        utils.saveText(descriptor, outputDirectory, descriptorFile)

        modulesPath =  f'HTTPServices/{self.Name}/Ext'

        self.saveModules(outputDirectory, modulesPath)

        pass