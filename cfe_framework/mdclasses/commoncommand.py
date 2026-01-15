import xml.etree.ElementTree as ET
import cfe_framework.utils as utils
from .genericV8Object import GenericV8Object


class CommonCommand(GenericV8Object):

    def __init__(self, name, synonym=None, id=None):
        super().__init__(name, synonym, id)

        self.Group = None

    def makeXMLDescriptor(self):

        metaDataNode = ET.Element("MetaDataOBject")
        commonCommandNode  = ET.Element("CommonCommand")
        commonCommandNode.attrib['uuid'] = self.UUID

        internalInfoBlock = ET.Element("InternalInfo")        
        self.generateInternalInfoBlock(internalInfoBlock)        
        commonCommandNode.append(internalInfoBlock)
        
        propertiesNode = ET.Element("Properties")
        
        self.generateCommonProperties(propertiesNode)
        commonCommandNode.append(propertiesNode)

        propertiesNode.append(utils.makeTextNode("Group", self.Group))

        metaDataNode.append(commonCommandNode)

        return utils.writeDocumentToString(metaDataNode, True)

    def serialize(self, outputDirectoryOrArchive):
        
        descriptor = self.makeXMLDescriptor()
        descriptorFile = f'CommonCommands/{self.Name}.xml'

        utils.saveText(descriptor, outputDirectoryOrArchive, descriptorFile)

        modulesPath = f'CommonCommands/{self.Name}/Ext'
        self.saveModules(outputDirectoryOrArchive, modulesPath)
