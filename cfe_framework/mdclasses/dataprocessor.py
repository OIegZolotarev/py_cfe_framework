from .genericV8Object import GenericV8Object
from .objectform import ObjectForm
from .modulekind import ModuleKind
from .typeproducing_object import TypeProducingObject
import cfe_framework.utils as utils
import uuid

import xml.etree.ElementTree as ET

# TODO: пересмотреть иерархию классов
# MetaDataObject -> GenericV8Object (с модулями и формами) -> TypeProducingV8Object (RDO и обработки?)
#                       |                                           |
#                   Команды, httpсервис и прочее                Константы, Обработки, Документы, Справочники
#
class DataProcessor(TypeProducingObject):
    
    def __init__(self, name, synonym=None, id=None):
        super().__init__(name, synonym, id)
        
        typeKinds = ['Object', 'Manager']
        self.declareGeneratedTypes(typeKinds)

        
    def serialize(self, outputDirectory):
        
        descriptor = self.makeDescriptorXML()
        descriptorFile = f'DataProcessors/{self.Name}.xml'

        extPath = f'DataProcessors/{self.Name}/Ext'

        utils.saveText(descriptor, outputDirectory, descriptorFile)

        self.saveModules(outputDirectory, extPath)
        
        pass
    
    def makeDescriptorXML(self):
        
        metaDataNode = ET.Element("MetaDataOBject")
        dataProcessorNode = ET.Element("DataProcessor")
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
        
        pass
    
