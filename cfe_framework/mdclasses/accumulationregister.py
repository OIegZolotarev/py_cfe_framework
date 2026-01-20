from .typeproducing_object import TypeProducingObject
from enum import Enum

import cfe_framework.utils as utils
import xml.etree.ElementTree as ET

class AccumulationRegisterTypes(Enum):
    Balance = 'Balance'
    Turnovers = 'Turnovers'
    
class AccumulationRegister(TypeProducingObject):

    def __init__(self, name, synonym=None, id=None):
        super().__init__(name, synonym, id)
        
        types = ['Record', 'Manager', 'Selection', 'List', 'RecordSet', 'RecordKey']
        self.declareGeneratedTypes(types)
        
        self.RegisterType = AccumulationRegisterTypes.Turnovers
        
    def makeDescriptorXML(self):

        metaDataNode = ET.Element("MetaDataOBject")
        accumulationRegisterNode = ET.Element("AccumulationRegister")
        accumulationRegisterNode.attrib['uuid'] = self.UUID

        internalInfoNode = ET.Element("InternalInfo")
        self.generateInternalInfoBlock(internalInfoNode)

        accumulationRegisterNode.append(internalInfoNode)

        propertiesNode = ET.Element("Properties")
        self.generateCommonProperties(propertiesNode)

        propertiesNode.append(utils.makeTextNode("RegisterType", self.RegisterType.value))
        
        accumulationRegisterNode.append(propertiesNode)

        childObjectsNode = ET.Element("ChildObjects")
        self.generateFormsDescriptors(childObjectsNode)
        accumulationRegisterNode.append(childObjectsNode)

        metaDataNode.append(accumulationRegisterNode)

        return utils.writeDocumentToString(metaDataNode, True)
    
    def serialize(self, outputDirectory):

        descriptor = self.makeDescriptorXML()
        descriptorFile = f'AccumulationRegisters/{self.Name}.xml'

        extPath = f'AccumulationRegisters/{self.Name}/Ext'

        utils.saveText(descriptor, outputDirectory, descriptorFile)

        self.saveModules(outputDirectory, extPath)

        formsPath = f'AccumulationRegisters/{self.Name}/Forms'
        self.saveForms(outputDirectory, formsPath)    