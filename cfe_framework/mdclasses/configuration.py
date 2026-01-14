from .metadataobject import MetaDataObject
from .language import Language
from .role import Role

from enum import Enum

import cfe_framework.utils as utils
import xml.etree.ElementTree as ET
import uuid

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
    
class InterfaceCompatibilityMode(Enum):
    Version8_2 = "Version8_2"
    Version8_2EnableTaxi = "Version8_2EnableTaxi"
    TaxiEnableVersion8_2 = "TaxiEnableVersion8_2"
    Taxi = "Taxi"

class Configuration(MetaDataObject):
    
    def __init__(self, name, prefix: str, synonym = None, id=None):
        super().__init__(name, synonym, id)
        
        self.NamePrefix = prefix        
        self.MainRole = None
        self.ChildObjects : list[MetaDataObject] = []
        
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

        self.Language : Language = None

    def registerObject(self, newObject : MetaDataObject) -> MetaDataObject:

        self.ChildObjects.append(newObject)
        return newObject

    def setLanguage(self, parentLangId = None, langName = None, langCode = None, langObject = None):

        if langObject == None:
            self.Language = self.registerObject(Language(langName, langCode))                        
        else:
            self.Language = langObject

        self.Language.ExtendedConfigurationObject = parentLangId

        
    def setMainRole(self, roleName : str, roleObject: Role = None):        
        
        if roleObject != None:
            self.MainRole = roleObject        
        else:
            self.MainRole = self.registerObject(Role(roleName))
                    
        pass
    
    def makeConfigurationXML(self):
        
        def makeApplicationUsePurposeNode():
    
            valNode = ET.Element("v8:Value")
            valNode.attrib['xsi:type'] = 'app:ApplicationUsePurpose'
            valNode.text = 'PlatformApplication'
            
            usePurposesNode = ET.Element("UsePurposes")
            usePurposesNode.append(valNode)
            
            return usePurposesNode

        def makeDefaultRolesNode():
            
            refNode = ET.Element('xr:Item')
            refNode.attrib['xsi:type'] = 'xr:MDObjectRef'
            refNode.text = 'Role.' + self.MainRole.Name
            
            defaultRolesNode = ET.Element('DefaultRoles')
            defaultRolesNode.append(refNode)
            
            return defaultRolesNode

        
        
        metaDataObjectNode = ET.Element("MetaDataObject")        
        metaDataObjectNode.attrib['version'] = utils.FORMAT_VERISON
        
        internalInfoNode = ET.Element("InternalInfo")
    
        magicIDS = utils.v8platformMagicalUIDSet()
        
        for id in magicIDS:
            
            randomId = str(uuid.uuid4())
            
            containedObjectNode = ET.Element("xr:ContainedObject")
            containedObjectNode.append(utils.makeTextNode("xr:ClassId", id))
            containedObjectNode.append(utils.makeTextNode("xr:ObjectId", randomId))
            
            internalInfoNode.append(containedObjectNode)
            
            
        configurationNode = ET.Element("Configuration")
        configurationNode.attrib["uuid"] = self.UUID        
        configurationNode.append(internalInfoNode)
        
        # Properties node
        propertiesNode = ET.Element("Properties")
        
        self.writeCommonFields(propertiesNode)
        
        propertiesNode.append(utils.makeTextNode("ConfigurationExtensionPurpose", self.ExtensionPurpose))
        propertiesNode.append(utils.makeTextNode("ObjectBelonging", "Adopted"))
        
        keepMappings = self.KeepMappingToExtendedConfigurationObjectsByIDs
        propertiesNode.append(utils.makeTextNode("KeepMappingToExtendedConfigurationObjectsByIDs", utils.booleanToString(keepMappings)))
        
        propertiesNode.append(utils.makeTextNode("NamePrefix", self.NamePrefix))
        
        mode = self.ConfigurationExtensionCompatibilityMode
        propertiesNode.append(utils.makeTextNode("ConfigurationExtensionCompatibilityMode", mode))
        
        propertiesNode.append(utils.makeTextNode("DefaultRunMode", "ManagedApplication"))
        
        propertiesNode.append(makeApplicationUsePurposeNode())
        
        propertiesNode.append(utils.makeTextNode("ScriptVariant", "Russian"))
        
        propertiesNode.append(makeDefaultRolesNode())
        
        propertiesNode.append(utils.makeTextNode("Vendor", self.Vendor))
        propertiesNode.append(utils.makeTextNode("Version", self.Version))
        
        if self.Language == None:
            raise Exception("Не указан основной язык конфигурации!")
        
        propertiesNode.append(utils.makeTextNode("DefaultLanguage", f"Language.{self.Language.Name}"))
        

        
        propertiesNode.append(utils.makeLocalizedTextNode("BriefInformation", self.BriefInformation))
        propertiesNode.append(utils.makeLocalizedTextNode("DetailedInformation", self.DetailedInformation))
        
        propertiesNode.append(utils.makeTextNode("Copyright", self.Copyright))
        propertiesNode.append(utils.makeTextNode("VendorInformationAddress", self.VendorInformationAddress))
        propertiesNode.append(utils.makeTextNode("ConfigurationInformationAddress", self.ConfigurationInformationAddress))
        
        propertiesNode.append(utils.makeTextNode("InterfaceCompatibilityMode", self.InterfaceCompatibilityMode))
        
        configurationNode.append(propertiesNode)
        
        # Properties node end
        
        # Child object start
    
        childObjectsNode = ET.Element("ChildObjects")
        
        for obj in self.ChildObjects:
            childObjectsNode.append(utils.makeTextNode(obj.ObjectClass, obj.Name))
            pass
        
        configurationNode.append(childObjectsNode)
    
        # Child object end
    
        metaDataObjectNode.append(configurationNode)
   
        return utils.writeDocumentToString(metaDataObjectNode, True)
        
        
       
    def serialize(self, outputDirectory):
        
        configurationXML = self.makeConfigurationXML()            
        utils.saveText(configurationXML, outputDirectory, "Configuration.xml")
        
        # TODO: Так ли нужен ConfigDumpInfo.xml ? Без него вполне неплохо работает на объемах расширения

        for obj in self.ChildObjects:
            obj.serialize(outputDirectory)

        if self.ManagedApplicationModule != None:
            utils.saveText(self.ManagedApplicationModule.encode('utf-8'), outputDirectory,  "Ext/ManagedApplicationModule.bsl")

        if self.ExternalConnectionModule != None:
            utils.saveText(self.ExternalConnectionModule.encode('utf-8'), outputDirectory,  "Ext/ExternalConnectionModule.bsl")            
        if self.SessionModule != None:
            utils.saveText(self.SessionModule.encode('utf-8'), outputDirectory,             "Ext/SessionModule.bsl")                        