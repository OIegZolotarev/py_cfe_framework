import zipfile

from mdclasses.modulekind import ModuleKind

from mdclasses.configuration import Configuration, ConfigurationExtensionCompatibilityMode 
from mdclasses.commonmodule import CommonModule
from mdclasses.catalog import Catalog
from mdclasses.commoncommand import CommonCommand
from mdclasses.commandgroup import CommandGroup
from mdclasses.httpservice import HTTPService

from mdclasses.constant import Constant

sampleCFE = Configuration("ЦАУ_Хотфиксы", "ЦАУ_", "Хотфиксы")

def testCommonModule(cfg: Configuration):

	commonModule = CommonModule("ТестовыйОбщийМодуль")
	

	commonModule.ModuleText = f"""

Процедура ПриветМир()
	// Модуль сгенерирован генератором патчей :)
	// f{commonModule}
	Сообщить("Здорова!");
КонецПроцедуры
"""

	cfg.registerObject(commonModule)

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

def testHTTPService(cfg: Configuration):

	service = HTTPService("HTTPСервис1")

	service.ExtendedConfigurationObject = '80e3bbff-85a6-4bc8-81c8-886ebd74254f'
	
	service.ExtendedModules[ModuleKind.Module] = f"""

	// Код HTTP сервиса сгенирован генератором патчей  :)
	// {service}
"""
	
	cfg.registerObject(service)

def testConstant(cfg: Configuration):

	constant = Constant('Константа1')
	constant.ExtendedConfigurationObject = 'edfc555a-9afe-4bfe-bced-3ebe46f3be80'

	constant.ExtendedModules[ModuleKind.ValueManagerModule] = f"""
&После("ПриветМир")
Процедура ЦАУ_ПриветМир()
	// Вставить содержимое метода.
	// {constant}
КонецПроцедуры
"""
	
	constant.ExtendedModules[ModuleKind.ManagerModule] = f"""
	// {constant}
"""

	cfg.registerObject(constant)

sampleCFE.setLanguage(langName="Русский", langCode="ru")
sampleCFE.setMainRole(roleName="ЦАУ_ОсновнаяРоль")
sampleCFE.ConfigurationExtensionCompatibilityMode = ConfigurationExtensionCompatibilityMode.Version8_3_27

testCatalog(sampleCFE)
testCommonCommand(sampleCFE)
testCommonModule(sampleCFE)
testHTTPService(sampleCFE)
testConstant(sampleCFE)


z = zipfile.ZipFile("C:/temp/patch.zip", 'w')
sampleCFE.serialize(z)
z.close()




pass