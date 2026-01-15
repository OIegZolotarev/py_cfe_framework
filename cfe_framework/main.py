import zipfile

from mdclasses.modulekind import ModuleKind

from mdclasses.configuration import Configuration, ConfigurationExtensionCompatibilityMode 
from mdclasses.commonmodule import CommonModule
from mdclasses.catalog import Catalog
from mdclasses.document import Document
from mdclasses.commoncommand import CommonCommand
from mdclasses.commandgroup import CommandGroup
from mdclasses.httpservice import HTTPService
from mdclasses.objectform import ObjectForm

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

	catalog = Catalog(name='Номенклатура')
	catalog = cfg.registerObject(catalog)
	catalog.ExtendedConfigurationObject = '4650d7a2-9fbd-4f4d-ba92-0dd21eca0856'

	text = """

	&Вместо("ПередЗаписью")
	Процедура Расш1_ПередЗаписью(Отказ)
		Сообщить("Генератор патчей :)"); 
	КонецПроцедуры

	"""

	catalog.ExtendedModules[ModuleKind.ObjectModule] = text
	catalog.ExtendedModules[ModuleKind.ManagerModule] = text

	form = ObjectForm("ФормаЭлемента")
	form.ExtendedConfigurationObject = '9be54424-2c12-4c3d-a36c-8b1f1f254bc4'

	form.ModuleText = f"""


&НаСервере    
&Вместо("ПриСозданииНаСервере")
Процедура ЦАУ_ПриСозданииНаСервере(Отказ, СтандартнаяОбработка)
	Сообщить("Модуль формы из генератора патчей {form}");
	
КонецПроцедуры


"""
	
	catalog.Forms.append(form)

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

def testDocument(cfg: Configuration):

	doc = Document('ТестовыйДокумент')
	doc.ExtendedConfigurationObject = '4b5bb55b-5053-4d11-bebc-d27a72b08ede'

	objectModuleText = f"// Текст модуля объекта сгененирован генератором патчей :) {doc}"
	managerModuleText = f"// Текст модуля менеджера сгененирован генератором патчей :) {doc}"

	doc.ExtendedModules[ModuleKind.ObjectModule] = objectModuleText
	doc.ExtendedModules[ModuleKind.ManagerModule] = managerModuleText

	form = ObjectForm("ФормаДокумента")
	form.ExtendedConfigurationObject = '01d685e0-257b-4a55-b162-4075efa080a2'

	form.ModuleText = f"""


&НаСервере    
&Вместо("ПриСозданииНаСервере")
Процедура ЦАУ_ПриСозданииНаСервере(Отказ, СтандартнаяОбработка)
	Сообщить("Модуль формы из генератора патчей {form}, {doc}");
	
КонецПроцедуры


"""
	
	doc.Forms.append(form)

	cfg.registerObject(doc)


sampleCFE.setLanguage(langName="Русский", langCode="ru")
sampleCFE.setMainRole(roleName="ЦАУ_ОсновнаяРоль")
sampleCFE.ConfigurationExtensionCompatibilityMode = ConfigurationExtensionCompatibilityMode.Version8_3_27

testCatalog(sampleCFE)
testCommonCommand(sampleCFE)
testCommonModule(sampleCFE)
testHTTPService(sampleCFE)
testConstant(sampleCFE)
testDocument(sampleCFE)


z = zipfile.ZipFile("C:/temp/patch.zip", 'w')
sampleCFE.serialize(z)
z.close()




pass