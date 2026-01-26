from .typeproducing_object import TypeProducingObject
from enum import Enum

import cfe_framework.utils as utils
import xml.etree.ElementTree as ET

class InformationRegister(TypeProducingObject):
    
    def __init__(self, name, synonym=None, id=None):            
        super().__init__(name, synonym, id)
        
        types = ['Record', 'Manager', 'Selection', 'List', 'RecordSet', 'RecordKey', 'RecordManager']
        self.declareGeneratedTypes(types)
        
    def makeDescriptorXML(self):
        
        metaDataNode = ET.Element("MetaDataOBject")
        informationRegisterNode = ET.Element("InformationRegister")
        informationRegisterNode.attrib['uuid'] = self.UUID

        internalInfoNode = ET.Element("InternalInfo")
        self.generateInternalInfoBlock(internalInfoNode)

        informationRegisterNode.append(internalInfoNode)

        propertiesNode = ET.Element("Properties")
        self.generateCommonProperties(propertiesNode)
   
        
        informationRegisterNode.append(propertiesNode)

        childObjectsNode = ET.Element("ChildObjects")
        self.generateFormsDescriptors(childObjectsNode)
        informationRegisterNode.append(childObjectsNode)

        metaDataNode.append(informationRegisterNode)

        return utils.writeDocumentToString(metaDataNode, True)
    
    def serialize(self, outputDirectory):

        descriptor = self.makeDescriptorXML()
        descriptorFile = f'InformationRegisters/{self.Name}.xml'

        extPath = f'InformationRegisters/{self.Name}/Ext'

        utils.saveText(descriptor, outputDirectory, descriptorFile)

        self.saveModules(outputDirectory, extPath)

        formsPath = f'InformationRegisters/{self.Name}/Forms'
        self.saveForms(outputDirectory, formsPath)    