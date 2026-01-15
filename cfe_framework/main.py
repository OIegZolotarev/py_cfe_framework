import zipfile

from mdclasses.configuration import Configuration, ConfigurationExtensionCompatibilityMode 
from mdclasses.commonmodule import CommonModule
from mdclasses.catalog import Catalog
from mdclasses.referencedatatype import ModuleKind

from mdclasses.commoncommand import CommonCommand
from mdclasses.commandgroup import CommandGroup

sampleCFE = Configuration("ЦАУ_Хотфиксы", "ЦАУ_", "Хотфиксы")

def testCatalog(cfg: Configuration):

	catalog = cfg.registerObject(Catalog(name='Номенклатура'))
	catalog.ExtendedConfigurationObject = '4650d7a2-9fbd-4f4d-ba92-0dd21eca0856'

	text = """

	&Вместо("ПередЗаписью")
	Процедура Расш1_ПередЗаписью(Отказ)
		Сообщить("Генератор патчей :)"); 
	КонецПроцедуры

	"""

	catalog.ExtendedModules[ModuleKind.ObjectModule] = text
	catalog.ExtendedModules[ModuleKind.ManagerModule] = text

def testCommonCommand(cfg: Configuration):

	
	commandGroup = CommandGroup("ГруппаКоманд1")
	commandGroup.ExtendedConfigurationObject = '99cf519a-cf46-4c98-a3ea-b7a0e3a31598'
	cfg.registerObject(commandGroup)


	text = """&НаКлиенте
&Вместо("ОбработкаКоманды")
Процедура ЦАУ_ОбработкаКоманды(ПараметрКоманды, ПараметрыВыполненияКоманды)
	Сообщить("Код загружен из генератора патчей :)")
КонецПроцедуры
"""
	cmd = CommonCommand("ОбщаяКоманда1")
	cmd.ExtendedConfigurationObject = '87bdf0e0-dd4f-4d61-882a-eee775f1ab44'

	cmd.ExtendedModules[ModuleKind.CommandModule] = text
	cmd.Group = 'CommandGroup.ГруппаКоманд1'

	cfg.registerObject(cmd)

sampleCFE.setLanguage(langName="Русский", langCode="ru")
sampleCFE.setMainRole(roleName="ЦАУ_ОсновнаяРоль")
sampleCFE.ConfigurationExtensionCompatibilityMode = ConfigurationExtensionCompatibilityMode.Version8_3_27

testCatalog(sampleCFE)
testCommonCommand(sampleCFE)


z = zipfile.ZipFile("C:/temp/patch.zip", 'w')
sampleCFE.serialize(z)
z.close()




pass