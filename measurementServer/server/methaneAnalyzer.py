from math import nan
from operator import mod
from pandas.core.frame import DataFrame
from scipy.interpolate.interpolate import interp1d
from measurementServer.calibration import CalibrationModel, CalibrationModelTemplate
from measurementServer.calibration.calibrationFunctions import *
from measurementServer.common import values
from ..common import *
from ..calibration import *
import csv
import os
import glob
import pandas as pd
import numpy as np
import datetime as dt

class MethaneAnalyzer:
    
    def __init__(self):        
        self.Vref = 1.024
        self.model1Templates = [CalibrationModelTemplate(function_name=key, dependence_function=values[0], predictor_names=values[1], dependent_name=values[2]) for key, values in calib1Functions.items()]
        self.model2Templates = [CalibrationModelTemplate(function_name=key, dependence_function=values[0], predictor_names=values[1], dependent_name=values[2]) for key, values in calib2Functions.items()]
        self.model3Templates = [CalibrationModelTemplate(function_name=key, dependence_function=values[0], predictor_names=values[1], dependent_name=values[2]) for key, values in calib3Functions.items()]

    def concatCsvIntoFrame(self, dirPath):
        all_files = []
        if os.path.isdir(dirPath):
            all_files = glob.glob(dirPath + "/*.csv")
        else:
            all_files = [dirPath]
        li = []
        for filename in all_files:
            df = pd.read_csv(filename, delimiter=',')
            li.append(df)
        frame = pd.concat(li, axis=0, ignore_index=True)
        frame_renamed = frame.rename(columns = ValuesNames.stringToName, inplace = False)
        return frame_renamed

    def appendRowToCsv(self, filename, listOfElements):
        with open(filename, 'a+', newline ='') as writeObj:
            writer = csv.writer(writeObj)
            writer.writerow(listOfElements)

    def getCalibratedModels(self, df, modelTemplates):

        modelsList = []
        for modelTemplate in modelTemplates:
            m = CalibrationModel(
                function_name=modelTemplate.function_name, 
                dependence_function=modelTemplate.function, 
                predictor_names=modelTemplate.predictor_names,
                dependent_name=modelTemplate.dependent_name
            )

            hasAllColumns = all([name in list(df.keys()) for name in (m.predictor_names + m.dependent_name)])
            if not hasAllColumns:
                continue

            X = {name: list(df[name]) for name in m.predictor_names}
            Y = (df[m.dependent_name[0]]).to_numpy()
            m.fit(X, Y)
            if np.isnan(m.coefficients).any():
                continue
            modelsList.append(m)

        return modelsList

    def calculateWithModel(self, df, model):

        hasAllColumns = all([name in list(df.keys()) for name in (model.predictor_names)])
        if not hasAllColumns:
            return None

        df_calc = df[model.predictor_names]
        df_result = model.calculate(df_calc)
        df[model.dependent_name[0]] = df_result
        return df

    def calibration(self, seriespath1, seriespath2, referencePath):
        # Загрузить данные
        df1 = self.concatCsvIntoFrame(seriespath1)
        df1[ValuesNames.voltage0.name] = df1[ValuesNames.voltage.name]
        step1models = self.getCalibratedModels(df1, self.model1Templates)

        # Подготовить данные
        df2 = self.concatCsvIntoFrame(seriespath2)
        df_Ch4_Ref = self.concatCsvIntoFrame(referencePath)
        df2 = self.interpolateCH4Data(df2, df_Ch4_Ref)
        df2[ValuesNames.ch4.name] = df2[ValuesNames.ch4Ref.name]

        # Создать массив готовых калибровок ResultModel и заполнить его
        dict_resultModels = []
        df_resultModels = DataFrame()
        # Рассчитать модели и сохранить их в массив
        for model1 in step1models:
            df_calc = self.calculateWithModel(df2, model1)
            df_calc = self.addRsR0(df_calc)
            step2models = self.getCalibratedModels(df_calc, self.model2Templates)
            for model2 in step2models:
                df_calc2 = self.calculateWithModel(df_calc, model2)
                df_calc2[ValuesNames.ch4LR.name] = df_calc2[ValuesNames.ch4Ref.name]
                step3models = self.getCalibratedModels(df_calc2, self.model3Templates)
                for model3 in step3models:
                    df_models = pd.concat([
                        self.modelToDataFrame(ModelNames.model1, model1),
                        self.modelToDataFrame(ModelNames.model2, model2),
                        self.modelToDataFrame(ModelNames.model3, model3)
                    ], axis=1)
                    df_resultModels = pd.concat([df_resultModels, df_models], axis=0, ignore_index=True)
                    dict_resultModels.append(
                        {
                         ModelNames.model1   : model1,
                         ModelNames.model2   : model2,
                         ModelNames.model3   : model3
                        }

                    )
        best_resultModel = self.findBestModel(df_resultModels)
        return df_resultModels, dict_resultModels, best_resultModel

    def findBestModel(self, df_resultModels):
        df_sorted = df_resultModels.sort_values(by=[ModelNames.model1+ModelParameters.rmse, ModelNames.model1+ModelParameters.adjusted_r_squared], ascending=[True, False], inplace=True)
        bestModelDict = {
            ModelNames.model1   : df_sorted.loc[0, ModelNames.model1],
            ModelNames.model2   : df_sorted.loc[0, ModelNames.model2],
            ModelNames.model3   : df_sorted.loc[0, ModelNames.model3]
        }
        return bestModelDict
    
    def modelToDataFrame(self, prefix, model : CalibrationModel):
        df = DataFrame(columns=
        [
         prefix + ModelParameters.function_name,
         prefix + ModelParameters.predictor_names,
         prefix + ModelParameters.dependent_name,
         prefix + ModelParameters.coefficients,
         prefix + ModelParameters.rmse,
         prefix + ModelParameters.adjusted_r_squared ])
        df.astype(
            {   
                prefix + ModelParameters.function_name      : str, 
                prefix + ModelParameters.predictor_names    : object,
                prefix + ModelParameters.dependent_name     : object,
                prefix + ModelParameters.coefficients       : object
            }
        )
        df.at[0, prefix + ModelParameters.function_name] = model.function_name
        df.at[0, prefix + ModelParameters.predictor_names] = model.predictor_names
        df.at[0, prefix + ModelParameters.dependent_name] = model.dependent_name
        df.at[0, prefix + ModelParameters.coefficients] = model.coefficients
        df.at[0, prefix + ModelParameters.rmse] = model.rmse
        df.at[0, prefix + ModelParameters.adjusted_r_squared] = model.adjusted_r_squared
        return df

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
        
        timestrings = df_calculated[ValuesNames.timestamp.name].to_numpy()
        timestamps = [dt.datetime.fromisoformat(s) for s in timestrings]
        ref_timestrings = df_reference[ValuesNames.timestamp.name].to_numpy()
        ref_timestamps = [dt.datetime.fromisoformat(s) for s in ref_timestrings]

        unix_times = self.convertTimestampsToFloats(timestamps)
        ref_unix_times = self.convertTimestampsToFloats(ref_timestamps)

        ch4_reference = df_reference[ValuesNames.ch4Ref.name].to_numpy()
        interploated_ch4_reference = self.interpolation(t=ref_unix_times, t_new=unix_times, ch4=ch4_reference)

        if not interploated_ch4_reference is None:
            df_calculated[ValuesNames.ch4Ref.name] = interploated_ch4_reference

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


