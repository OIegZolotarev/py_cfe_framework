from .metadataobject import MetaDataObject
from .referencedatatype import ModuleKind
import xml.etree.ElementTree as ET
import cfe_framework.utils as utils

class GenericV8Object(MetaDataObject):

    def __init__(self, name, synonym = None, id=None):
        super().__init__(name, synonym, id)

        self.ExtendedModules : dict[ModuleKind, str]
        self.ExtendedModules = {} 

    def serialize(self, outputDirectory):
        return super().serialize(outputDirectory)
    
    def generateInternalInfoBlock(self, block: ET.Element):

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