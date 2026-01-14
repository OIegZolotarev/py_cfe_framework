import utils
from xml.etree.ElementTree import ElementTree as ET
from mdclasses.metadataobject import MetaDataObject

class Language(MetaDataObject):
    
    def __init__(self, name, langCode):
        super().__init__(name)        
        self.LanguageCode = langCode
    
    def serialize(self, outputDirectory):
        
        xmlText = self.makeXMLDescriptor() 
        
        # TODO: проверить существование каталога
        
        targetFile = f'{{outputDirectory}}/Languages/{self.Name}.xml'
        
        f = open(targetFile, 'wt')
        f.write(xmlText)
        f.close()

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
        
        # TODO: уместен ли захардкоженный id здесь?
        propertiesNode.append(utils.makeTextNode("ExtendedConfigurationObject", '874fead0-d1f1-4826-a60d-eb068f566abd'))
        
        languageNode.append(propertiesNode)
        
        metadataObjectNode.append(languageNode)    
        return utils.writeDocumentToString(metadataObjectNode, True)   
            
        