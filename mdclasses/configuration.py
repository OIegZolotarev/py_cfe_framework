from mdclasses.metadataobject import MetaDataObject
from enum import Enum

class ExtensionPurpose(Enum):
    
    Customization = "Customization"
    AddOn = "AddOn"
    Patch = "Patch"

class ConfigurationExtensionCompatibilityMode(Enum):
    
    Version8_3_20 = "Version8_3_20"
    Version8_3_21 = "Version8_3_21"
    Version8_3_22 = "Version8_3_22"
    Version8_3_23 = "Version8_3_23"
    Version8_3_24 = "Version8_3_24"
    Version8_3_25 = "Version8_3_25"
    Version8_3_26 = "Version8_3_26"
    Version8_3_27 = "Version8_3_27"
    
class InterfaceCompatibilityMode:
    Version8_2 = "Version8_2"
    Version8_2EnableTaxi = "Version8_2EnableTaxi"
    TaxiEnableVersion8_2 = "TaxiEnableVersion8_2"
    Taxi = "Taxi"

class Configuration(MetaDataObject):
    
    def __init__(self, name, prefix: str, synonym = None, id=None):
        super().__init__(name, synonym, id)
        
        self.NamePrefix = prefix        
        self.MainRole = None
        self.ChildObjects = []
        
        self.ExtensionPurpose = ExtensionPurpose.Patch
        
        self.KeepMappingToExtendedConfigurationObjectsByIDs = True
        
        self.ManagedApplicationModule  = None
        self.SessionModule             = None
        self.ExternalConnectionModule  = None
        
        self.ConfigurationExtensionCompatibilityMode = ConfigurationExtensionCompatibilityMode.Version8_3_24
        self.InterfaceCompatibilityMode = InterfaceCompatibilityMode.Taxi
        
        # Сведения о разработке.
        
        self.Vendor = ''
        self.Version = '1.0.0.0'
    
        self.BriefInformation = 'Автоматически сгенерированный патч из репозитория'
        self.DetailedInformation = ''
    
        self.Copyright = ''
        self.VendorInformationAddress = ''
        self.ConfigurationInformationAddress = ''
        
        
    def setMainRole(self, roleName : str, generateNew: bool = False):        
        
        self.MainRole = roleName
        
        if generateNew:
            # TODO
            pass
        
        pass
    
    
    
    
    def serialize(self, outputDirectory):
        
        
        
        return super().serialize(outputDirectory)