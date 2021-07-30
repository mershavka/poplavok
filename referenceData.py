from enums import MeasureType
from datetime import datetime as dt
from typing import Optional

class ReferenceData:

    def __init__(self, seriesId, loadingDate):
        self.seriesId = seriesId
        self.loadingDate = loadingDate