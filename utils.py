import uuid
import xml.etree.ElementTree as ET

FORMAT_VERISON = "2.11"

def setupNamespaceDescriptions():    
    ET.register_namespace("","http://v8.1c.ru/8.3/MDClasses")
    ET.register_namespace("app","http://v8.1c.ru/8.2/managed-application/core")
    ET.register_namespace("cfg","http://v8.1c.ru/8.1/data/enterprise/current-config")
    ET.register_namespace("cmi","http://v8.1c.ru/8.2/managed-application/cmi")
    ET.register_namespace("ent","http://v8.1c.ru/8.1/data/enterprise")
    ET.register_namespace("lf","http://v8.1c.ru/8.2/managed-application/logform")
    ET.register_namespace("style","http://v8.1c.ru/8.1/data/ui/style")
    ET.register_namespace("sys","http://v8.1c.ru/8.1/data/ui/fonts/system")
    ET.register_namespace("v8","http://v8.1c.ru/8.1/data/core")
    ET.register_namespace("v8ui","http://v8.1c.ru/8.1/data/ui")
    ET.register_namespace("web","http://v8.1c.ru/8.1/data/ui/colors/web")
    ET.register_namespace("win","http://v8.1c.ru/8.1/data/ui/colors/windows")
    ET.register_namespace("xen","http://v8.1c.ru/8.3/xcf/enums")
    ET.register_namespace("xpr","http://v8.1c.ru/8.3/xcf/predef")
    ET.register_namespace("xr","http://v8.1c.ru/8.3/xcf/readable")
    ET.register_namespace("xs","http://www.w3.org/2001/XMLSchema")
    ET.register_namespace("xsi","http://www.w3.org/2001/XMLSchema-instance")  
    
def hackNamespaces(node: ET.Element):        
    node.attrib["xmlns"] = "http://v8.1c.ru/8.3/MDClasses"    
    node.attrib["xmlns:app"] = "http://v8.1c.ru/8.2/managed-application/core"
    node.attrib["xmlns:cfg"] = "http://v8.1c.ru/8.1/data/enterprise/current-config"
    node.attrib["xmlns:cmi"] = "http://v8.1c.ru/8.2/managed-application/cmi"
    node.attrib["xmlns:ent"] = "http://v8.1c.ru/8.1/data/enterprise"
    node.attrib["xmlns:lf"] = "http://v8.1c.ru/8.2/managed-application/logform"
    node.attrib["xmlns:style"] = "http://v8.1c.ru/8.1/data/ui/style"
    node.attrib["xmlns:sys"] = "http://v8.1c.ru/8.1/data/ui/fonts/system"
    node.attrib["xmlns:v8"] = "http://v8.1c.ru/8.1/data/core"
    node.attrib["xmlns:v8ui"] = "http://v8.1c.ru/8.1/data/ui"
    node.attrib["xmlns:web"] = "http://v8.1c.ru/8.1/data/ui/colors/web"
    node.attrib["xmlns:win"] = "http://v8.1c.ru/8.1/data/ui/colors/windows"
    node.attrib["xmlns:xen"] = "http://v8.1c.ru/8.3/xcf/enums"
    node.attrib["xmlns:xpr"] = "http://v8.1c.ru/8.3/xcf/predef"
    node.attrib["xmlns:xr"] = "http://v8.1c.ru/8.3/xcf/readable"
    node.attrib["xmlns:xs"] = "http://www.w3.org/2001/XMLSchema"
    node.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"         


def writeDocumentToString(doc: ET.ElementTree, addNamespace = False):
    
    if addNamespace:
        hackNamespaces(doc)
    
    ET.indent(doc, space="  ", level=0)
    xml_string = ET.tostring(doc, encoding='unicode', xml_declaration=True)
    return xml_string    

def makeTextNode(nodeName : str, nodeText : str) -> ET.Element:
    
    element = ET.Element(nodeName)
    element.text = nodeText
    
    return element

def makeLocalizedTextNode(wrappedNode, nodeText : str, nodeName = 'v8:item', nodeLang = 'ru'):
    
    
    
    itemNode = ET.Element(nodeName)
    
    itemNode.append(makeTextNode('v8:lang', nodeLang.strip()))
    itemNode.append(makeTextNode('v8:content', nodeText))
    
    result = ET.Element(wrappedNode)
    result.append(itemNode)
    
    return result

def booleanToString(val):
    return "true" if val else "false"

def makeNameSynonimCommentNode(parentNode : ET.Element, data):
    
    parentNode.append(makeTextNode("Name", data['Name']))
    
    parentNode.append(makeLocalizedTextNode("Synonym",data['Synonym']))
    
    parentNode.append(makeTextNode("Comment", data["Comment"]))

def makeTypeDescriptionNode(types : list, nodeName = 'Type'):
    # TODO implement later
    pass

def v8platformMagicalUIDSet() -> list[str]:
    result = []
    
    result.append("9cd510cd-abfc-11d4-9434-004095e12fc7")
    result.append("9fcd25a0-4822-11d4-9414-008048da11f9")
    result.append("e3687481-0a87-462c-a166-9f34594f9bba")
    result.append("9de14907-ec23-4a07-96f0-85521cb6b53b")
    result.append("51f2d5d8-ea4d-4064-8892-82951750031e")
    result.append("e68182ea-4237-4383-967f-90c1e3370bc7")
    result.append("fb282519-d103-4dd3-bc12-cb271d631dfc")
    
    return result

def v8ClassNameDict():
    result = {}
    
    result["ГруппаКоманд"] = "CommandGroup"
    result["ОбщаяКартинка"] = "CommonPicture"
    result["ОбщаяКоманда"] = "CommonCommand"
    result["ОбщийМакет"] = "CommonTemplate"
    result["ОбщийМодуль"] = "CommonModule"
    result["ОбщаяФорма"] = "CommonForm"
    result["ПараметрСеанса"] = "SessionParameter"
    result["ПодпискаНаСобытие"] = "EventSubscription"
    result["Подсистема"] = "Subsystem"
    result["Роль"] = "Role"
    result["Язык"] = "Language"    

    return result

def standartCommandGroupsDict():
    # TODO: implement later
    result = {}
    return result

def getClassNameExtension(className):
    
    if className == 'ОбщаяКоманда' or className == 'CommonCommand':
        return 'CommandModule'
    elif className == 'ОбщаяФорма' or className == 'CommonForm':
        return "Form"
    elif className == 'ОбщийМодуль' or className == 'CommonModule':
        return "Module"
    elif className == 'ОбщаяКартинка' or className == 'CommonPicture':
        return "Picture"
    elif className == 'ОбщийМакет' or className == 'CommonTemplate':
        return "Template"
    elif className == 'Роль' or className == 'Role':
        return "Rights"
    else:
        return ""

def initObjectData(objectClass: str, objectName: str, synonym: str, comment: str) -> dict:
    
    result = {}
    result["ObjectClass"]       = objectClass
    result["Name"]              = objectName.strip()
    result["Synonym"]           = makeDescriptionFromName(objectName) if objectName else ""
    result["Comment"]           = comment.strip
    result["id"]                = uuid.uuid5()
    result["HasData"]           = False
    result["FormatVersion"]     = FORMAT_VERISON
	
    return result

def filterObjectByClass(objects: list[dict], objectClass: str):    
    return [obj for obj in objects if obj['ObjectClass'] == objectClass]

def makeDescriptionFromName(name: str) -> str:
    
    if not name:
        return ""
    
    result = []
    current_word = name[0]
    
    for i, char in enumerate(name[1:], 1):
        prev_char = name[i-1]
        
        # Определяем, нужно ли начинать новое слово
        is_new_word = (
            char.isupper() and not char.isdigit()  # переход в CamelCase
            or char.isupper() and prev_char.islower()  # Заглавная после строчной
            or char.isdigit() and not prev_char.isdigit()  # Цифра после буквы
            or not char.isdigit() and prev_char.isdigit()  # Буква после цифры
        )
        
        if is_new_word:
            result.append(current_word)
            current_word = char
        else:
            current_word += char
    
    result.append(current_word)
    
    # Преобразуем в нижний регистр, но сохраняем аббревиатуры (если все буквы заглавные)
    words = []
    for word in result:
        if word.isupper() and len(word) > 1:
            words.append(word)  # Оставляем аббревиатуры как есть
        else:
            words.append(word.lower())
    
    # Первое слово делаем с заглавной буквы
    if words:
        words[0] = words[0].capitalize()
    
    return ' '.join(words)

def initExtensionData(confName: str, prefix: str, id: None):
    
    result = {}
    
    result['Name'] = confName
    result['Synonym'] = makeDescriptionFromName(confName)
    result['Comment'] = ''
    
    result['ExtensionID'] = id if id != None else str(uuid.uuid4())
    result['MainRole'] = prefix + 'ОсновнаяРоль'
    result['Objects'] = []
    
    result['ManagedApplicationModule']  = None
    result['SessionModule']             = None
    result['ExternalConnectionModule']  = None
    
    # Customization, AddOn, Patch
    result['ExtensionPurpose'] = 'Patch'
    
    # Всегда true?
    result['KeepMappingToExtendedConfigurationObjectsByIDs'] = True
    
    result['NamePrefix'] = prefix
    
    result['ConfigurationExtensionCompatibilityMode'] = 'Version8_3_24'
    
    result['Vendor'] = ''
    result['Version'] = '1.0.0.0'
    
    result['BriefInformation'] = 'Автоматически сгенерированный патч из репозитория'
    result['DetailedInformation'] = ''
    
    result['Copyright'] = ''
    result['VendorInformationAddress'] = ''
    result['ConfigurationInformationAddress'] = ''
    
    # Version8_2, Version8_2EnableTaxi, TaxiEnableVersion8_2, Taxi
    result['InterfaceCompatibilityMode'] = 'Taxi'
    
    return result

def initLangData(name : str, code: str):
    
    result = {}
    
    result['Name'] = name
    result['LanguageCode'] = code
    result['Id'] = str(uuid.uuid4())
    
    return result