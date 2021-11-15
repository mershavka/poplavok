from operator import mod
from scipy.interpolate.interpolate import interp1d
from measurementServer.calibration import CalibrationModel, CalibrationModelTemplate
from measurementServer.calibration.calibrationFunctions import *
from measurementServer.common import values
from ..common import *
from ..calibration import *
import csv
import glob
import pandas as pd
import numpy as np
import datetime as dt

class methaneAnalyzer:
    
    def __init__(self):        
        self.Vref = 1.024
        self.model1Templates = [CalibrationModelTemplate(dependence_function=func[0], predictor_names=func[1], dependent_name=func[2]) for func in calib1Functions.values()]
        self.model2Templates = [CalibrationModelTemplate(dependence_function=func[0], predictor_names=func[1], dependent_name=func[2]) for func in calib2Functions.values()]
        self.model3Templates = [CalibrationModelTemplate(dependence_function=func[0], predictor_names=func[1], dependent_name=func[2]) for func in calib3Functions.values()]

    def concatCsvIntoFrame(self, dirPath):
        all_files = glob.glob(dirPath + "/*.csv")
        li = []
        for filename in all_files:
            df = pd.read_csv(filename, delimiter=',')
            li.append(df)
        frame = pd.concat(li, axis=0, ignore_index=True)
        #Изменить названия колонок
        return frame

    def appendRowToCsv(self, filename, listOfElements):
        with open(filename, 'a+', newline ='') as writeObj:
            writer = csv.writer(writeObj)
            writer.writerow(listOfElements)

    def getCalibratedModels(self, df, modelTemplates):

        modelsList = []
        for modelTemplate in modelTemplates:
            m = CalibrationModel(modelTemplate.function, modelTemplate.predictor_names, modelTemplate.dependent_name)

            hasAllColumns = all([name in list(df.keys()) for name in (m.predictor_names + m.dependent_name)])
            if not hasAllColumns:
                continue

            X = {name: list(df[name]) for name in m.predictor_names}
            m.fit(X, list(df[m.dependent_name]))
            modelsList.append(m)

        return modelsList

    def calculateWithModel(self, df, model):

        hasAllColumns = all([name in list(df.keys()) for name in (model.predictor_names + model.dependent_name)])
        if not hasAllColumns:
            return None

        df_calc = df[model.predictor_names]
        df[model.dependent_name] = model.calculate(df_calc)
        return df

    def calibration(self, seriespath1, seriespath2, referencePath):
        # Загрузить данные
        df1 = self.concatCsvIntoFrame(seriespath1)
        step1models = self.getCalibratedModels(df1, self.model1Templates)

        df2 = self.concatCsvIntoFrame(seriespath2)
        df_Ch4_Ref = self.concatCsvIntoFrame(referencePath)
        df2 = self.interpolateCH4Data(df2, df_Ch4_Ref)

        for model in step1models:
            df_calc = self.calculateWithModel(df2, model)
            df_calc = self.addRsR0(df_calc)
            step2models = self.getCalibratedModels(df_calc, self.model2Templates)

        # Получить лучшую модель?

        pass



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

    def interpolateCH4Data(self, df_calculated, df_reference) -> np.ndarray:
        
        timestamps = df_calculated[ValuesNames.timestamp.name].to_numpy()
        ref_timestamps = df_reference[ValuesNames.timestamp.name].to_numpy()
        unix_times = self.convertTimestampsToFloats(timestamps)
        ref_unix_times = self.convertTimestampsToFloats(ref_timestamps)

        ch4_reference = df_reference[ValuesNames.ch4Ref.name].to_numpy()
        interploated_ch4_reference = self.interpolation(t=ref_unix_times, t_new=unix_times, ch4=ch4_reference)

        if interploated_ch4_reference:
            df_calculated[values.ValuesNames.ch4Ref.name] = interploated_ch4_reference

        return df_calculated

        # new_array = np.column_stack((timestamps, interploated_ch4_reference))
        # df = pd.DataFrame(data=new_array, columns=[ValuesNames.timestamp.getString(), ValuesNames.ch4Ref.getString()])
        # path = ref_ch4_dirPath + "/ch4_ref_interpolated_{}.csv".format(dt.datetime.now().strftime(timeformat))
        # df.to_csv(path, sep=",", index=False, header=df.columns)

    def prepareAndTransferData(self, ):
        pass

    def calculateCH4withModel(self, model: calibrationModel.CalibrationModel, dataDict):
        pass

    def addRsR0(self, df):        
        df[ValuesNames.rsr0.name] = RsR0_calc(df) 
        return df


