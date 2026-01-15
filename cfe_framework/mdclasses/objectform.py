import uuid
import cfe_framework.utils as utils
import xml.etree.ElementTree as ET
from .metadataobject import MetaDataObject

class ObjectForm:

    def __init__(self, name: str = None, moduleText: str = None, synonym = None, comment = None):

        self.Name = name
        self.Synonym = synonym if synonym else utils.makeDescriptionFromName(name)
        self.Comment = comment if comment else ''
        self.ExtendedConfigurationObject = None        
        self.ModuleText = moduleText

        self.UUID = str(uuid.uuid4())
        

        pass

    def makeDummyFormUIDescriptor(self):
        formNode = ET.Element("Form")
        return utils.writeDocumentToString(formNode, True)
    
    def makeXMLDescriptor(self):

        metaDataObjectNode = ET.Element("MetaDataObject")

        formNode = ET.Element("Form")
        formNode.attrib['uuid'] = self.UUID

        internalInfoNode = ET.Element('InternalInfo')             
        internalInfoNode.append(utils.makePropertyStateNode("Form", "Extended"))
        formNode.append(internalInfoNode)

        propertiesNode = ET.Element("Properties")

        if self.ExtendedConfigurationObject != None:
            propertiesNode.append(utils.makeTextNode("ObjectBelonging", "Adopted"))
            propertiesNode.append(utils.makeTextNode("ExtendedConfigurationObject", self.ExtendedConfigurationObject))
        
        propertiesNode.append(utils.makeTextNode("Name", self.Name))
        propertiesNode.append(utils.makeTextNode("Comment", self.Comment))
        propertiesNode.append(utils.makeLocalizedTextNode("Synonym", self.Synonym))

        # Надеюсь это не поменяется на моем веку.
        propertiesNode.append(utils.makeTextNode("FormType", "Managed"))

        formNode.append(propertiesNode)

        metaDataObjectNode.append(formNode)
        return utils.writeDocumentToString(metaDataObjectNode, True)

    def serialize(self, outputDirectoryOrArchive, formsDirectory):

        descriptor = self.makeXMLDescriptor()
        descriptorFile = f'{formsDirectory}/{self.Name}.xml'
        utils.saveText(descriptor, outputDirectoryOrArchive, descriptorFile)

        dummyUIFile = f'{formsDirectory}/{self.Name}/Ext/Form.xml'
        utils.saveText(self.makeDummyFormUIDescriptor(), outputDirectoryOrArchive, dummyUIFile)

        moduleFile = f'{formsDirectory}/{self.Name}/Ext/Form/Module.bsl'
        utils.saveText(self.ModuleText, outputDirectoryOrArchive, moduleFile)

        pass
