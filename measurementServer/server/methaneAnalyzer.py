from scipy.interpolate.interpolate import interp1d
from measurementServer.calibration import calibrationModel
from measurementServer.calibration.calibrationFunctions import *
from ..common import *
from ..calibration import *
import csv
import glob
import pandas as pd
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
            df = pd.read_csv(filename, delimiter=',')
            li.append(df)
        frame = pd.concat(li, axis=0, ignore_index=True)
        return frame

    def appendRowToCsv(self, filename, listOfElements):
        with open(filename, 'a+', newline ='') as writeObj:
            writer = csv.writer(writeObj)
            writer.writerow(listOfElements)


    def passDataToCalibrationModule(self, series1Path, series2Path):
        models = self.calibrationModelsPreparing()
        series1Data = self

    def convertTimestampsToFloats(self, times: np.ndarray) -> np.ndarray:
        return np.array([t.timestamp() for t in times])

    def convertFloatsToTimestamps(self, times: np.ndarray):
        return dt.datetime.fromtimestamp(times)


    def interpolation(self, t:np.ndarray, ch4:np.ndarray, t_new:np.ndarray) -> np.ndarray:
        if isinstance(t, np.ndarray) and isinstance(ch4, np.ndarray) and isinstance(t_new, np.ndarray):
            ch4_new = np.interp(t_new, t, ch4)
            return ch4_new
        return None

    def interpolateCH4Data(self, ch4_dirPath, ref_ch4_dirPath) -> np.ndarray:
        df_reference = self.concatCsvIntoFrame(ref_ch4_dirPath)
        df_calculated = self.concatCsvIntoFrame(ch4_dirPath)

        timestamps = df_calculated[ValuesNames.timestamp.getString()].to_numpy()
        ref_timestamps = df_reference[ValuesNames.timestamp.getString()].to_numpy()
        unix_times = self.convertTimestampsToFloats(timestamps)
        ref_unix_times = self.convertTimestampsToFloats(ref_timestamps)

        ch4_reference = df_reference[ValuesNames.ch4Ref.getString()].to_numpy()
        interploated_ch4_reference = self.interpolation(t=ref_unix_times, t_new=unix_times, ch4=ch4_reference)

        if interploated_ch4_reference:
            new_array = np.column_stack((timestamps, interploated_ch4_reference))
            df = pd.DataFrame(data=new_array, columns=[ValuesNames.timestamp.getString(), ValuesNames.ch4Ref.getString()])
            path = ref_ch4_dirPath + "/ch4_ref_interpolated_{}.csv".format(dt.datetime.now().strftime(timeformat))
            df.to_csv(path, sep=",", index=False, header=df.columns)

        return interploated_ch4_reference

    def prepareAndTransferData(self, ):
        pass

    def calculateCH4withModel(self, model: calibrationModel.CalibrationModel, dataDict):
        
