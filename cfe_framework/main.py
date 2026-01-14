import zipfile
from mdclasses.configuration import Configuration, ConfigurationExtensionCompatibilityMode 
from mdclasses.commonmodule import CommonModule


test = Configuration("ЦАУ_Хотфиксы", "ЦАУ_", "Хотфиксы")

# parentLangId - идентификатор языка из расширяемой конфигурации
# , parentLangId='97d26151-6744-4347-b444-4403757b3ae8'
test.setLanguage(langName="Русский", langCode="ru")
test.setMainRole(roleName="ЦАУ_ОсновнаяРоль")
test.ConfigurationExtensionCompatibilityMode = ConfigurationExtensionCompatibilityMode.Version8_3_27

module = CommonModule("ЦАУ_ОбщийМодуль")
module.ModuleText = """

Процедура ПриветМир() Экспорт
    Сообщить("Привет мир");
КонецПроцедуры

"""
test.registerObject(module)

test.ManagedApplicationModule = """
&После("ПриНачалеРаботыСистемы")
Процедура ЦАУ_ПриНачалеРаботыСистемы()
	
	Сообщить("Ext generated from python!");	
	
КонецПроцедуры

"""

#z = zipfile.ZipFile("test.zip", 'w')
#test.serialize(z)
#z.close()

test.serialize("sandbox")


pass