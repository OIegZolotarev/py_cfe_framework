import uuid
import utils

import xml.etree.ElementTree as ET

class MetaDataObject:
    
    def __init__(self, name: str, synonym : str = None, id = None):
        
        self.Name = name
        self.Synonym = synonym if synonym else utils.makeDescriptionFromName(name)
        self.Comment = ''
        self.UUID = id if id else str(uuid.uuid4())
        self.ObjectClass = ''

        self.ObjectClass = type(self).__name__
        self.ExtendedConfigurationObject = None
        
        pass
    
    
    def serialize(self, outputDirectory):
        pass
    
    def writeCommonFields(self, parentNode: ET.Element):
        
        parentNode.append(utils.makeTextNode("Name", self.Name))    
        parentNode.append(utils.makeLocalizedTextNode("Synonym", self.Synonym))    
        parentNode.append(utils.makeTextNode("Comment", self.Comment))
        
        pass