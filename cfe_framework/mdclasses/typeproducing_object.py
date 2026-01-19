from .genericV8Object import GenericV8Object

from .modulekind import ModuleKind
from .objectform import ObjectForm

import cfe_framework.utils as utils
import uuid

import xml.etree.ElementTree as ET

class TypeProducingObject(GenericV8Object):
    
    
    def __init__(self, name, synonym=None, id=None):
        super().__init__(name, synonym, id)
        
        self.GeneratedTypes = {}
        
        
        self.ExtendedModules : dict[ModuleKind, str]
        self.ExtendedModules = {} 
        
        self.Forms: list[ObjectForm]
        self.Forms = []    
        
        
    def declareGeneratedTypes(self, typeKinds):                

        for kind in typeKinds:
            self.GeneratedTypes[kind] = f'{self.ObjectClass}{kind}.{self.Name}'
            
    def generateInternalInfoBlock(self, block):
        
        super().generateInternalInfoBlock(block)
        
        for kind, type in self.GeneratedTypes.items():
            
            typeId =  uuid.uuid4()
            valueId = uuid.uuid4()

            generatedTypeNode = ET.Element("xr:GeneratedType")

            generatedTypeNode.append(utils.makeTextNode("xr:TypeId", typeId))
            generatedTypeNode.append(utils.makeTextNode("xr:ValueId", valueId))

            generatedTypeNode.attrib['name'] = type
            generatedTypeNode.attrib['category'] = kind

            block.append(generatedTypeNode)
            
    def generateFormsDescriptors(self, childObjectsNode: ET.Element):

        for form in self.Forms:
            childObjectsNode.append(utils.makeTextNode("Form", form.Name))            

    def saveForms(self, outputDirectoryOrArchive, filesPath: str):

        for form in self.Forms:            
            form.serialize(outputDirectoryOrArchive, filesPath)            
 
    
      