import xml.etree.ElementTree as ET
import cfe_framework.utils as utils
from  .objectform import ObjectForm

from .metadataobject import MetaDataObject
from enum import Enum
import uuid

from .modulekind import ModuleKind


class ReferenceDataType(MetaDataObject):

    def __init__(self, name, synonym = None, id=None):
        super().__init__(name, synonym, id)

        self.GeneratedTypes = {}

        typeKinds = ['Object', 'Ref', 'Selection', 'List', 'Manager']

        for kind in typeKinds:
            self.GeneratedTypes[kind] = f'{self.ObjectClass}{kind}.{self.Name}'

        pass

        self.ExtendedModules : dict[ModuleKind, str]
        self.ExtendedModules = {} 

        self.Forms: list[ObjectForm]
        self.Forms = []

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

        pass

    def saveModules(self, outputDirectoryOrArchive, destPath):

        for moduleKind, moduleText in self.ExtendedModules.items():

            if moduleText == None:
                continue
            
            fileName = f'{destPath}/{moduleKind.value}.bsl'
            utils.saveText(moduleText, outputDirectoryOrArchive, fileName)


    def generateFormsDescriptors(self, childObjectsNode: ET.Element):

        for form in self.Forms:
            childObjectsNode.append(utils.makeTextNode("Form", form.Name))            

    def saveForms(self, outputDirectoryOrArchive, filesPath: str):

        for form in self.Forms:            
            form.serialize(outputDirectoryOrArchive, filesPath)            