import xml.etree.ElementTree as ET

import cfe_framework.utils as utils
from .genericV8Object import GenericV8Object

class CommandGroup(GenericV8Object):

    def __init__(self, name, synonym=None, id=None):
        super().__init__(name, synonym, id)

        self.Category = "NavigationPanel"
    
    def makeXMLDescriptor(self):

        metaDataObjectNode = ET.Element("MetaDataObject")

        commandGroupNode = ET.Element("CommandGroup")
        commandGroupNode.attrib['uuid'] = self.UUID

        commandGroupNode.append(ET.Element("InternalInfo"))

        propertiesNode = ET.Element("Properties")        
        self.generateCommonProperties(propertiesNode)
        propertiesNode.append(utils.makeTextNode("Category", self.Category))
        commandGroupNode.append(propertiesNode)

        metaDataObjectNode.append(commandGroupNode)
        
        return utils.writeDocumentToString(metaDataObjectNode, True)

    def serialize(self, outputDirectory):
        
        descriptor = self.makeXMLDescriptor()
        descriptorFile = f'CommandGroups/{self.Name}.xml'

        utils.saveText(descriptor,outputDirectory, descriptorFile)

    