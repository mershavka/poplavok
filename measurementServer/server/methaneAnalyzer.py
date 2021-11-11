from scipy.interpolate.interpolate import interp1d
from measurementServer.calibration import calibrationModel
from measurementServer.calibration.calibrationFunctions import *
from ..common import *
from ..calibration import *
import csv
import glob
import pandas
import numpy as np
import datetime as dt

class methaneAnalyzer:
    
    def __init__(self):
        
        self.model1Templates = [calibrationModel(func[0], func[1]) for func in calib1Functions.values()]
        self.model2Templates = [calibrationModel(func[0], func[1]) for func in calib2Functions.values()]
        self.model3Templates = [calibrationModel(func[0], func[1]) for func in calib3Functions.values()]

    def concatCsvIntoFrame(self, dirPath):
        all_files = glob.glob(dirPath + "/*.csv")
        li = []
        for filename in all_files:
            df = pandas.read_csv(filename, delimiter=',')
            li.append(df)
        frame = pandas.concat(li, axis=0, ignore_index=True)
        return frame

    def appendRowToCsv(self, filename, listOfElements):
        with open(filename, 'a+', newline ='') as writeObj:
            writer = csv.writer(writeObj)
            writer.writerow(listOfElements)


    def passDataToCalibrationModule(self, series1Path, series2Path):
        models = self.calibrationModelsPreparing()
        series1Data = self

    def convertTimestampsToFloats(self, times: np.ndarray):
        return np.array([t.timestamp() for t in times])

    def convertFloatsToTimestamps(self, times: np.ndarray):
        return dt.datetime.fromtimestamp(times)


    def interpolation(self, t:np.ndarray, ch4:np.ndarray, t_new:np.ndarray):
        if isinstance(t, np.ndarray) and isinstance(ch4, np.ndarray) and isinstance(t_new, np.ndarray):
            ch4_new = np.interp(t_new, t, ch4)
            return ch4_new
        return None

    def prepareCH4Data(self, ch4_dirPath, ref_ch4_dirPath):
        df_reference = self.concatCsvIntoFrame(ref_ch4_dirPath)
        df_calculated = self.concatCsvIntoFrame(ch4_dirPath)

        unix_times = self.convertTimestampsToFloats(df_calculated[ValuesNames.timestamp.getString()].to_numpy())
        ref_unix_times = self.convertTimestampsToFloats(df_reference[ValuesNames.timestamp.getString()].to_numpy())

        ch4_reference = df_reference[ValuesNames.ch4Ref.getString()].to_numpy()
        ch4_calculated = df_calculated[ValuesNames.ch4.getString()].to_numpy()

        # interploated_ch4 = self.interpolation(t=unix_times, t_new=ref_unix_times, ch4=ch4_calculated)
        interploated_ch4_reference = self.interpolation(t=ref_unix_times, t_new=unix_times, ch4=ch4_reference)

        

        pass



