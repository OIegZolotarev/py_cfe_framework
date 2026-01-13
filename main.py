import utils
import uuid
import serializer

def saveText(name, text):
    
    f = open(name, 'wt')
    f.write(text)
    f.close()

extData = utils.initExtensionData("ЦАУ_ИзмененияИзEDT","ЦАУ_", str(uuid.uuid4()))

conf_xml = serializer.buildConfigurationXML(extData)
conf_dump_xml = serializer.buildConfigDumpInfoXML(extData)

saveText("Configuration.xml", conf_xml)
saveText("ConfigDumpInfo.xml", conf_dump_xml)

pass