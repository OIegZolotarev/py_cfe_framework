from .metadataobject import MetaDataObject
from enum import Enum

class ModuleKind(Enum):
    
    ObjectModule            = "ObjectModule"
    ManagerModule           = "ManagerModule"
    FormModule              = "Module"
    CommandModule           = "CommandModule"
    RecordSetModule         = "RecordSetModule"
    ValueManagerModule      = "ValueManagerModule"    

    Module                  = "Module"