from .typeproducing_object import TypeProducingObject

import cfe_framework.utils as utils
import xml.etree.ElementTree as ET


class AccountingRegister(TypeProducingObject):

    def __init__(self, name, synonym=None, id=None):
        super().__init__(name, synonym, id)
        
        types = ['Record', 'ExtDimensions', 'RecordSet', 'RecordKey', 'Selection', 'List', 'Manager']
        self.declareGeneratedTypes(types)
        
        self.Correspondence = None

    def makeDescriptorXML(self):

        metaDataNode = ET.Element("MetaDataOBject")
        AccountingRegisterNode = ET.Element("AccountingRegister")
        AccountingRegisterNode.attrib['uuid'] = self.UUID

        internalInfoNode = ET.Element("InternalInfo")
        self.generateInternalInfoBlock(internalInfoNode)

        AccountingRegisterNode.append(internalInfoNode)

        propertiesNode = ET.Element("Properties")
        self.generateCommonProperties(propertiesNode)
       
        
        AccountingRegisterNode.append(propertiesNode)

        childObjectsNode = ET.Element("ChildObjects")
        self.generateFormsDescriptors(childObjectsNode)
        AccountingRegisterNode.append(childObjectsNode)

        metaDataNode.append(AccountingRegisterNode)

        return utils.writeDocumentToString(metaDataNode, True)
    
    def serialize(self, outputDirectory):

        descriptor = self.makeDescriptorXML()
        descriptorFile = f'AccountingRegisters/{self.Name}.xml'

        extPath = f'AccountingRegisters/{self.Name}/Ext'

        utils.saveText(descriptor, outputDirectory, descriptorFile)

        self.saveModules(outputDirectory, extPath)

        formsPath = f'AccountingRegisters/{self.Name}/Forms'
        self.saveForms(outputDirectory, formsPath)            