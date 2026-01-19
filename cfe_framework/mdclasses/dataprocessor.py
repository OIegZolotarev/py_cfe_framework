from .genericV8Object import GenericV8Object
from .objectform import ObjectForm
from .modulekind import ModuleKind
from .metadataobject import MetaDataObject
import cfe_framework.utils as utils
import uuid

import xml.etree.ElementTree as ET

# TODO: пересмотреть иерархию классов
# MetaDataObject -> GenericV8Object (с модулями и формами) -> TypeProducingV8Object (RDO и обработки?)
#                       |                                           |
#                   Команды, httpсервис и прочее                Константы, Обработки, Документы, Справочники
#
class DataProcessor(MetaDataObject):
    
    def __init__(self, name, synonym=None, id=None):
        super().__init__(name, synonym, id)

        self.ExtendedModules : dict[ModuleKind, str]
        self.ExtendedModules = {} 
        
        self.Forms: list[ObjectForm]
        self.Forms = []
        
        self.GeneratedTypes = {}
        typeKinds = ['Object', 'Manager']

        for kind in typeKinds:
            self.GeneratedTypes[kind] = f'{self.ObjectClass}{kind}.{self.Name}'
        
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
    
    def saveForms(self, outputDirectoryOrArchive, filesPath: str):

        for form in self.Forms:            
            form.serialize(outputDirectoryOrArchive, filesPath)                
            
    def generateFormsDescriptors(self, childObjectsNode: ET.Element):

        for form in self.Forms:
            childObjectsNode.append(utils.makeTextNode("Form", form.Name))            
            
    def generateInternalInfoBlock(self, block: ET.Element):

        for kind, type in self.GeneratedTypes.items():
            
            typeId =  uuid.uuid4()
            valueId = uuid.uuid4()

            generatedTypeNode = ET.Element("xr:GeneratedType")

            generatedTypeNode.append(utils.makeTextNode("xr:TypeId",        typeId))
            generatedTypeNode.append(utils.makeTextNode("xr:ValueId",       valueId))

            generatedTypeNode.attrib['name'] = type
            generatedTypeNode.attrib['category'] = kind

            block.append(generatedTypeNode)

        for kind, module in self.ExtendedModules.items():
            
            if module == None:
                continue

            propertyStateNode = ET.Element("xr:PropertyState")            

            propertyStateNode.append(utils.makeTextNode("xr:Property",      kind.value))
            propertyStateNode.append(utils.makeTextNode("xr:State",         "Extended"))

            block.append(propertyStateNode)

        pass            
    
    def saveModules(self, outputDirectoryOrArchive, destPath):

        for moduleKind, moduleText in self.ExtendedModules.items():

            if moduleText == None:
                continue
            
            fileName = f'{destPath}/{moduleKind.value}.bsl'
            utils.saveText(moduleText, outputDirectoryOrArchive, fileName)