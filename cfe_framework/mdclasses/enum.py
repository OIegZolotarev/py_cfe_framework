import xml.etree.ElementTree as ET
import cfe_framework.utils as utils

from .typeproducing_object import TypeProducingObject


class Enum(TypeProducingObject):
    
    def __init__(self, name, synonym=None, id=None):
        super().__init__(name, synonym, id)

        typeKinds = ['Ref', 'List', 'Manager']
        self.declareGeneratedTypes(typeKinds)

    def makeDescriptorXML(self):

        metaDataNode = ET.Element("MetaDataOBject")
        enumNode = ET.Element("Enum")
        enumNode.attrib['uuid'] = self.UUID

        internalInfoNode = ET.Element("InternalInfo")
        self.generateInternalInfoBlock(internalInfoNode)

        enumNode.append(internalInfoNode)

        propertiesNode = ET.Element("Properties")
        self.generateCommonProperties(propertiesNode)
        
        enumNode.append(propertiesNode)

        childObjectsNode = ET.Element("ChildObjects")
        self.generateFormsDescriptors(childObjectsNode)
        enumNode.append(childObjectsNode)

        metaDataNode.append(enumNode)

        return utils.writeDocumentToString(metaDataNode, True)
    
    def serialize(self, outputDirectory):

        descriptor = self.makeDescriptorXML()
        descriptorFile = f'Enums/{self.Name}.xml'

        extPath = f'Enums/{self.Name}/Ext'

        utils.saveText(descriptor, outputDirectory, descriptorFile)

        self.saveModules(outputDirectory, extPath)

        formsPath = f'Enums/{self.Name}/Forms'
        self.saveForms(outputDirectory, formsPath)            