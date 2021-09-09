from series import Series
import sys
import Pyro4
import Pyro4.util
from enums import *
from series import Series
from measurement import Measurement

Pyro4.util.SerializerBase.register_class_to_dict(Series, Series.toJson)
Pyro4.util.SerializerBase.register_class_to_dict(Measurement, Measurement.toJson)
Pyro4.util.SerializerBase.register_dict_to_class(Series, Series.fromJson)
Pyro4.util.SerializerBase.register_dict_to_class(Measurement, Measurement.fromJson)

sys.excepthook = Pyro4.util.excepthook
pyro_measurement_server = Pyro4.Proxy("PYRONAME:PyroMeasurementServer")    # use name server object lookup uri shortcut
# uri = input("Enter the uri of the warehouse: ").strip()
# pyro_measurement_server = Pyro4.Proxy(uri)
print(pyro_measurement_server.getSeriesList())