import uuid
import xml.etree.ElementTree as ET
import utils

from mdclasses.language import Language

def makeApplicationUsePurposeNode():
    
    valNode = ET.Element("v8:value")
    valNode.attrib['xsi:type'] = 'app:ApplicationUsePurpose'
    valNode.text = 'PlatformApplication'
    
    usePurposesNode = ET.Element("UsePurposes")
    usePurposesNode.append(valNode)
    
    return usePurposesNode

def makeDefaultRolesNode(extensionData : dict):
    
    refNode = ET.Element('xr:Item')
    refNode.attrib['xsi:type'] = 'xr:MDObjectRef'
    refNode.text = 'Role.' + extensionData['MainRole']
    
    defaultRolesNode = ET.Element('DefaultRoles')
    defaultRolesNode.append(refNode)
    
    return defaultRolesNode

def makeMetadataNode(objectName: str, id, version):
    metadataNode = ET.Element("Metadata")

    metadataNode.attrib['name']             = objectName
    
    if type(id) == str:
        metadataNode.attrib['id']               = id
    else:
        metadataNode.attrib['id']               = str(id)
        
    if type(version) == str:
        metadataNode.attrib['configVersion']    = version
    else:
        metadataNode.attrib['configVersion']    = str(version)
    
    return metadataNode

def saveConfigurationObjects(extensionData):
    
    for obj in extensionData['Objects']:
        
        #match(obj['ObjectClass']):
            #case 'Role':
         
        pass       
    
    pass

def buildLanguageDescriptorXML(language: Language):
    
    metadataObjectNode = ET.Element("MetaDataObject")
    metadataObjectNode.attrib['version'] = utils.FORMAT_VERISON
    
    languageNode = ET.Element("Language")
    
    languageNode.attrib["uuid"] = langData['Id']
    
    languageNode.append(ET.Element("InternalInfo"))
    
    propertiesNode = ET.Element("Properties")
    propertiesNode.append(utils.makeTextNode("Name",langData['Name']))
    propertiesNode.append(utils.makeTextNode("ObjectBelonging", "Adopted"))
    propertiesNode.append(utils.makeTextNode("LanguageCode", langData['LanguageCode']))
    
    # TODO: уместен ли захардкоженный id здесь?
    propertiesNode.append(utils.makeTextNode("ExtendedConfigurationObject", '874fead0-d1f1-4826-a60d-eb068f566abd'))
    
    languageNode.append(propertiesNode)
    
    metadataObjectNode.append(languageNode)    
    return utils.writeDocumentToString(metadataObjectNode, True)    

def buildRoleDescriptorXML(roleData):
    
    metadataObjectNode = ET.Element("MetaDataObject")
    metadataObjectNode.attrib['version'] = utils.FORMAT_VERISON
        
    roleNode = ET.Element("Role")    
    roleNode.attrib['uuid'] = roleData['Id']
    
    propetiesNode = ET.Element("Properties")
    utils.makeNameSynonimCommentNode(propetiesNode, roleData)
    
    roleNode.append(propetiesNode)
    
    metadataObjectNode.append(roleNode)        
    return utils.writeDocumentToString(metadataObjectNode, True)    
    

def buildConfigDumpInfoXML(extensionData: dict):

    # writeDocumentToString запишет декларацию XML
    
    configVersionsNode = ET.Element("ConfigVersions")
    
    for object in extensionData['Objects']:
        
        # TODO: сделать хеширование на основе фактических данных объекта?
        version = uuid.uuid4() 
               
        metadataNode = makeMetadataNode(f"{object['ObjectClass']}.{object['Name']}", object[id], version)        
        configVersionsNode.append(metadataNode)
        
        if object['HasData'] == True:
            
            nameExt = utils.getClassNameExtension(object['ObjectClass'])
            idExt = '.0'
            			
			
            name = f"{object['ObjectClass']}.{object['Name']}"
            
            if nameExt:
                name += '.' + nameExt
            
            metadataNode = makeMetadataNode(name, str(object['id']) + idExt, version)                
            configVersionsNode.append(metadataNode)
        
        pass
    
    keys = ['ManagedApplicationModule', 'SessionModule', 'ExternalConnectionModule']
    
    for moduleName in keys:    
        if extensionData[moduleName] != None:
            
            moduleData = extensionData[moduleName]
            
            # TODO: сделать хеширование на основе фактических данных объекта?
            version = uuid.uuid4() 
            name = f"Configuration.{extensionData['Name']}.{moduleName}"                       
            
            metadataNode = makeMetadataNode(name, moduleData['id'], version)                
            configVersionsNode.append(metadataNode)
    
    version = uuid.uuid4() 
    name = f"Configuration.{extensionData['Name']}"
    
    # TODO: возможно надо хранить версию расширения...
    confId = extensionData['ExtensionID']
    metadataNode = makeMetadataNode(name, confId, version)                
    configVersionsNode.append(metadataNode)
    
    configDumpInfoNode = ET.Element("ConfigDumpInfo")
    
    configDumpInfoNode.attrib['format'] = 'Hierarchical'
    configDumpInfoNode.attrib['version'] = utils.FORMAT_VERISON
    
    configDumpInfoNode.append(configVersionsNode)
        
    return utils.writeDocumentToString(configDumpInfoNode)

def buildConfigurationXML(extensionData: dict):
        
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
    configurationNode.attrib["uuid"] = extensionData["ExtensionID"]
    configurationNode.append(internalInfoNode)
    
    # Properties node
    propertiesNode = ET.Element("Properties")
    
    utils.makeNameSynonimCommentNode(propertiesNode, extensionData)
    
    propertiesNode.append(utils.makeTextNode("ConfigurationExtensionPurpose", extensionData["ExtensionPurpose"]))
    propertiesNode.append(utils.makeTextNode("ObjectBelonging", "Adopted"))
    
    keepMappings = extensionData['KeepMappingToExtendedConfigurationObjectsByIDs']
    propertiesNode.append(utils.makeTextNode("KeepMappingToExtendedConfigurationObjectsByIDs", utils.booleanToString(keepMappings)))
    
    propertiesNode.append(utils.makeTextNode("NamePrefix", extensionData['NamePrefix']))
    
    mode = extensionData['ConfigurationExtensionCompatibilityMode']
    propertiesNode.append(utils.makeTextNode("ConfigurationExtensionCompatibilityMode", mode))
    
    propertiesNode.append(utils.makeTextNode("DefaultRunMode", "ManagedApplication"))
    
    propertiesNode.append(makeApplicationUsePurposeNode())
    
    propertiesNode.append(utils.makeTextNode("ScriptVariant", "Russian"))
    
    propertiesNode.append(makeDefaultRolesNode(extensionData))
    
    propertiesNode.append(utils.makeTextNode("Vendor", extensionData['Vendor']))
    propertiesNode.append(utils.makeTextNode("Version", extensionData['Version']))
    
    propertiesNode.append(utils.makeTextNode("DefaultLanguage", "Language.Русский"))
    
    propertiesNode.append(utils.makeLocalizedTextNode("BriefInformation", extensionData["BriefInformation"]))
    propertiesNode.append(utils.makeLocalizedTextNode("DetailedInformation", extensionData["DetailedInformation"]))
    
    propertiesNode.append(utils.makeTextNode("Copyright",extensionData["Copyright"]))
    propertiesNode.append(utils.makeTextNode("VendorInformationAddress",extensionData["VendorInformationAddress"]))
    propertiesNode.append(utils.makeTextNode("ConfigurationInformationAddress",extensionData["ConfigurationInformationAddress"]))
    
    propertiesNode.append(utils.makeTextNode("InterfaceCompatibilityMode",extensionData["InterfaceCompatibilityMode"]))
    
    configurationNode.append(propertiesNode)
    
    # Properties node end
    
    # Child object start
    
    childObjectsNode = ET.Element("ChildObjects")
    
    for obj in extensionData['Objects']:
        childObjectsNode.appeend(utils.makeTextNode(obj['ObjectClass'], obj['Name']))
        pass
    
    configurationNode.append(childObjectsNode)
    
    # Child object end
    
    metaDataObjectNode.append(configurationNode)
    
    
    
    return utils.writeDocumentToString(metaDataObjectNode, True)