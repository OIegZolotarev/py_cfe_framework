import xml.etree.ElementTree as ET

import cfe_framework.utils as utils
from .metadataobject import MetaDataObject
from .modulekind import ModuleKind

import uuid

class Constant(MetaDataObject):

    def __init__(self, name, synonym = None, id=None):
        super().__init__(name, synonym, id)

        self.GeneratedTypes = {}

        typeKinds = ['Manager', 'ValueManager', 'ValueKey']

        for kind in typeKinds:
            self.GeneratedTypes[kind] = f'{self.ObjectClass}{kind}.{self.Name}'

        pass

        self.ExtendedModules : dict[ModuleKind, str]
        self.ExtendedModules = {} 
        self.Type = None

    def generateInternalInfoBlock(self, block: ET.Element):

        for kind, type in self.GeneratedTypes.items():
            
            typeId =  uuid.uuid4()
            valueId = uuid.uuid4()

            generatedTypeNode = ET.Element("xr:GeneratedType")

            generatedTypeNode.append(utils.makeTextNode("xr:TypeId", typeId))
            generatedTypeNode.append(utils.makeTextNode("xr:ValueId", valueId))

            generatedTypeNode.attrib['name'] = type
            generatedTypeNode.attrib['category'] = kind

            block.append(generatedTypeNode)

        for kind, module in self.ExtendedModules.items():
            
            if module == None:
                continue

            propertyStateNode = ET.Element("xr:PropertyState")            

            propertyStateNode.append(utils.makeTextNode("xr:Property", kind.value))
            propertyStateNode.append(utils.makeTextNode("xr:State", "Extended"))

            block.append(propertyStateNode)

        # 2) Сохранить заимствования модулей.

        pass

    def saveModules(self, outputDirectoryOrArchive, destPath):

        for moduleKind, moduleText in self.ExtendedModules.items():

            if moduleText == None:
                continue
            
            fileName = f'{destPath}/{moduleKind.value}.bsl'
            utils.saveText(moduleText, outputDirectoryOrArchive, fileName)

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