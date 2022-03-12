# -*- coding: utf-8 -*-
from pinform import Measurement
from pinform.fields import FloatField


class Inside(Measurement):
  class Meta:
    measurement_name = 'inside'

  in_temp = FloatField(null=False)
  in_hum = FloatField(null=False)
  soil_hum = FloatField(null=False)
 
class Outside(Measurement):
  class Meta:
    measurement_name = 'outside'

  out_temp = FloatField(null=False)
  out_hum = FloatField(null=False)
  door = FloatField(null=False)

class Deposit(Measurement):
  class Meta:
    measurement_name = 'deposit'

  water_temp = FloatField(null=False)
  pump = FloatField(null=False)

class Climat(Measurement):
  class Meta:
    measurement_name = 'climat'

  ventilation = FloatField(null=False)
  heating = FloatField(null=False)
  refrigeration = FloatField(null=False)

class Irrigation(Measurement):
  class Meta:
    measurement_name = 'irrigation'

  min_soil_hum = FloatField(null=False)
  irrig_time = FloatField(null=False)

class ClimatControl(Measurement):
  class Meta:
    measurement_name = 'climatControl'

  min_temp = FloatField(null=False)
  target_temp = FloatField(null=False)
  max_temp = FloatField(null=False)
  min_hum = FloatField(null=False)
  max_hum = FloatField(null=False)
