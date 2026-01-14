import zipfile
from mdclasses.configuration import Configuration, ConfigurationExtensionCompatibilityMode


test = Configuration("ЦАУ_Хотфиксы", "ЦАУ_", "Хотфиксы")

# parentLangId - идентификатор языка из расширяемой конфигурации
# , parentLangId='97d26151-6744-4347-b444-4403757b3ae8'
test.setLanguage(langName="Русский", langCode="ru")
test.setMainRole(roleName="ЦАУ_ОсновнаяРоль")
test.ConfigurationExtensionCompatibilityMode = ConfigurationExtensionCompatibilityMode.Version8_3_27

z = zipfile.ZipFile("test.zip", 'w')
test.serialize(z)

z.close()


pass