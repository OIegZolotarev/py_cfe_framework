import xml.etree.ElementTree as ET
import cfe_framework.utils as utils

from .typeproducing_object import TypeProducingObject


class Report(TypeProducingObject):

    def __init__(self, name, synonym=None, id=None):
        super().__init__(name, synonym, id)

        typeKinds = ['Object', 'Manager']
        self.declareGeneratedTypes(typeKinds)


    def serialize(self, outputDirectoryOrArchive):
        
        descriptor = self.makeDescriptorXML()
        descriptorFile = f'Reports/{self.Name}.xml'

        extPath = f'Reports/{self.Name}/Ext'

        utils.saveText(descriptor, outputDirectoryOrArchive, descriptorFile)

        self.saveModules(outputDirectoryOrArchive, extPath)
        
        formsPath = f'Reports/{self.Name}/Forms'
        self.saveForms(outputDirectoryOrArchive, formsPath)
        
        pass
    
    def makeDescriptorXML(self):
        
        metaDataNode = ET.Element("MetaDataOBject")
        dataProcessorNode = ET.Element("Report")
        dataProcessorNode.attrib['uuid'] = self.UUID

        internalInfoNode = ET.Element("InternalInfo")
        self.generateInternalInfoBlock(internalInfoNode)
        dataProcessorNode.append(internalInfoNode)

        propertiesNode = ET.Element("Properties")
        self.generateCommonProperties(propertiesNode)

        dataProcessorNode.append(propertiesNode)

        childObjectsNode = ET.Element("ChildObjects")
        self.generateFormsDescriptors(childObjectsNode)
        dataProcessorNode.append(childObjectsNode)

        metaDataNode.append(dataProcessorNode)

        return utils.writeDocumentToString(metaDataNode, True)

