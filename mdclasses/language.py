import utils
import xml.etree.ElementTree as ET
from mdclasses.metadataobject import MetaDataObject

class Language(MetaDataObject):
    
    def __init__(self, name, langCode):
        super().__init__(name)              
        self.LanguageCode = langCode
    
    def serialize(self, outputDirectory):
        
        xmlText = self.makeXMLDescriptor()                 
        targetFile = f'Languages/{self.Name}.xml'

        utils.saveText(xmlText, outputDirectory, targetFile)


    def makeXMLDescriptor(self):
        metadataObjectNode = ET.Element("MetaDataObject")
        metadataObjectNode.attrib['version'] = utils.FORMAT_VERISON
        
        languageNode = ET.Element("Language")
        
        languageNode.attrib["uuid"] = self.UUID
        
        languageNode.append(ET.Element("InternalInfo"))
        
        propertiesNode = ET.Element("Properties")
        propertiesNode.append(utils.makeTextNode("Name", self.Name))
        propertiesNode.append(utils.makeTextNode("ObjectBelonging", "Adopted"))
        propertiesNode.append(utils.makeTextNode("LanguageCode", self.LanguageCode))

        if self.ExtendedConfigurationObject != None:
            propertiesNode.append(utils.makeTextNode("ExtendedConfigurationObject", self.ExtendedConfigurationObject))
        
        languageNode.append(propertiesNode)
        
        metadataObjectNode.append(languageNode)    
        return utils.writeDocumentToString(metadataObjectNode, True)   
            
        