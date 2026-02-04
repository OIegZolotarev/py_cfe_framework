import xml.etree.ElementTree as ET
import cfe_framework.utils as utils

from .typeproducing_object import TypeProducingObject


class BusinessProcess(TypeProducingObject):
    
    def __init__(self, name, synonym=None, id=None):
        super().__init__(name, synonym, id)

        typeKinds = ['Object', 'Ref', 'Selection', 'List', 'Manager', 'RoutePointRef']
        self.declareGeneratedTypes(typeKinds)

    def makeDescriptorXML(self):

        metaDataNode = ET.Element("MetaDataOBject")
        BusinessProcessNode = ET.Element("BusinessProcess")
        BusinessProcessNode.attrib['uuid'] = self.UUID

        internalInfoNode = ET.Element("InternalInfo")
        self.generateInternalInfoBlock(internalInfoNode)

        BusinessProcessNode.append(internalInfoNode)

        propertiesNode = ET.Element("Properties")
        self.generateCommonProperties(propertiesNode)
        
        BusinessProcessNode.append(propertiesNode)

        childObjectsNode = ET.Element("ChildObjects")
        self.generateFormsDescriptors(childObjectsNode)
        BusinessProcessNode.append(childObjectsNode)

        metaDataNode.append(BusinessProcessNode)

        return utils.writeDocumentToString(metaDataNode, True)
    
    def serialize(self, outputDirectory):

        descriptor = self.makeDescriptorXML()
        descriptorFile = f'BusinessProcesses/{self.Name}.xml'

        extPath = f'BusinessProcesses/{self.Name}/Ext'

        utils.saveText(descriptor, outputDirectory, descriptorFile)

        self.saveModules(outputDirectory, extPath)

        formsPath = f'BusinessProcesses/{self.Name}/Forms'
        self.saveForms(outputDirectory, formsPath)            