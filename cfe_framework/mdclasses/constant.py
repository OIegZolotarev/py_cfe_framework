import xml.etree.ElementTree as ET

import cfe_framework.utils as utils
from .metadataobject import MetaDataObject
from .modulekind import ModuleKind

import uuid

from .typeproducing_object import TypeProducingObject

class Constant(TypeProducingObject):

    def __init__(self, name, synonym = None, id=None):
        super().__init__(name, synonym, id)

        self.declareGeneratedTypes(['Manager', 'ValueManager', 'ValueKey'])
        self.Type = None


    def makeDescriptorXML(self):

        metaDataNode = ET.Element("MetaDataOBject")
        constantNode = ET.Element("Constant")
        constantNode.attrib['uuid'] = self.UUID

        internalInfoNode = ET.Element("InternalInfo")
        self.generateInternalInfoBlock(internalInfoNode)

        constantNode.append(internalInfoNode)

        propertiesNode = ET.Element("Properties")
        self.generateCommonProperties(propertiesNode)

        constantNode.append(propertiesNode)

        metaDataNode.append(constantNode)

        return utils.writeDocumentToString(metaDataNode, True)

    def serialize(self, outputDirectory):

        descriptor = self.makeDescriptorXML()
        descriptorFile = f'Constants/{self.Name}.xml'

        extPath = f'Constants/{self.Name}/Ext'

        utils.saveText(descriptor, outputDirectory, descriptorFile)

        self.saveModules(outputDirectory, extPath)