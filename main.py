import utils
import uuid
import serializer
from mdclasses.configuration import Configuration


test = Configuration("ЦАУ_Хотфиксы", "ЦАУ_", "Хотфиксы")

test.setMainRole("ОсновнаяРоль", True)
test.serialize('sandbox')

pass