import xml.etree.ElementTree  as ET
from .referencedatatype import ReferenceDataType, ModuleKind

import cfe_framework.utils as utils

class Document(ReferenceDataType):

    def __init__(self, name, synonym=None, id=None):
        super().__init__(name, synonym, id)

        self.ExtendedModules[ModuleKind.ObjectModule] = None
        self.ExtendedModules[ModuleKind.ManagerModule] = None

        pass

    def makeDescriptorXML(self):

        metaDataNode = ET.Element("MetaDataOBject")
        DocumentNode = ET.Element("Document")
        DocumentNode.attrib['uuid'] = self.UUID

        internalInfoNode = ET.Element("InternalInfo")
        self.generateInternalInfoBlock(internalInfoNode)

        DocumentNode.append(internalInfoNode)

        propertiesNode = ET.Element("Properties")
        self.generateCommonProperties(propertiesNode)

        DocumentNode.append(propertiesNode)

        childObjectsNode = ET.Element("ChildObjects")
        self.generateFormsDescriptors(childObjectsNode)
        DocumentNode.append(childObjectsNode)

        metaDataNode.append(DocumentNode)

        return utils.writeDocumentToString(metaDataNode, True)


    def serialize(self, outputDirectory):

        descriptor = self.makeDescriptorXML()
        descriptorFile = f'Documents/{self.Name}.xml'

        extPath = f'Documents/{self.Name}/Ext'

        utils.saveText(descriptor, outputDirectory, descriptorFile)

        self.saveModules(outputDirectory, extPath)

        formsPath = f'Documents/{self.Name}/Forms'
        self.saveForms(outputDirectory, formsPath)

