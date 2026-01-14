import uuid
import utils

class MetaDataObject:
    
    def __init__(self, name: str, synonym : str = None, id = None):
        
        self.Name = name
        self.Synonym = synonym if synonym else utils.makeDescriptionFromName(name)
        self.Comment = ''
        self.UUID = id if id else str(uuid.uuid4())
        
        pass
    
    
    def serialize(self, outputDirectory):
        pass