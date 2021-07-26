from enums import MeasureType
from datetime import datetime as dt
from typing import Optional

class ReferenceData:

    def __init__(self, seriesId, duration, periodicity, date, description: str ="", type: MeasureType = MeasureType.CALIBRATION_2):
        self.seriesId = seriesId
        self.duration = duration
        self.periodicity = periodicity
        self.date = date
        self.description = description
        self.type = type