import xml.etree.ElementTree  as ET
from .referencedatatype import ReferenceDataType, ModuleKind

import cfe_framework.utils as utils

class Catalog(ReferenceDataType):

    def __init__(self, name, synonym=None, id=None):
        super().__init__(name, synonym, id)

        self.ExtendedModules[ModuleKind.ObjectModule] = None
        self.ExtendedModules[ModuleKind.ManagerModule] = None

        pass

    def makeDescriptorXML(self):

        metaDataNode = ET.Element("MetaDataOBject")
        catalogNode = ET.Element("Catalog")
        catalogNode.attrib['uuid'] = self.UUID

        internalInfoNode = ET.Element("InternalInfo")
        self.generateInternalInfoBlock(internalInfoNode)

        catalogNode.append(internalInfoNode)

        propertiesNode = ET.Element("Properties")
        self.generateCommonProperties(propertiesNode)

        catalogNode.append(propertiesNode)

        childObjectsNode = ET.Element("ChildObjects")
        catalogNode.append(childObjectsNode)

        metaDataNode.append(catalogNode)

        return utils.writeDocumentToString(metaDataNode, True)


    def serialize(self, outputDirectory):

        descriptor = self.makeDescriptorXML()
        descriptorFile = f'Catalogs/{self.Name}.xml'

        extPath = f'Catalogs/{self.Name}/Ext'

        utils.saveText(descriptor, outputDirectory, descriptorFile)

        self.saveModules(outputDirectory, extPath)

