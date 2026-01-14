import utils
import xml.etree.ElementTree as ET
from mdclasses.metadataobject import MetaDataObject

class Role(MetaDataObject):
    
    def __init__(self, name, synonym = None, id=None):
        super().__init__(name, synonym, id)
        
        self.Rights = []

    def makeRoleXML(self):

        metadataObjectNode = ET.Element("MetaDataObject")

        propertiesNode = ET.Element("Properties")
        self.writeCommonFields(propertiesNode)
        

        roleNode = ET.Element("Role")        
        roleNode.attrib["uuid"] = self.UUID

        roleNode.append(propertiesNode)
        
        metadataObjectNode.append(roleNode)
        
        return utils.writeDocumentToString(metadataObjectNode, True)

    def serialize(self, outputDirectory):

        mdDescriptionFile = f'Roles/{self.Name}.xml'
        mdDescriptionText = self.makeRoleXML()

        utils.saveText(mdDescriptionText, outputDirectory, mdDescriptionFile)

        if len(self.Rights) > 0:
            
            rightsFile = f'Roles/{self.Name}/rights.xml'

            rightsText = '' # TODO

            utils.saveText(rightsText, outputDirectory, rightsFile)


        pass
        

    