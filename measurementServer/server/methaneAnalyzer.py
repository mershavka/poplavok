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
import random
from math import exp

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
        dict_resultModels = {}
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
                    df_models['id'] = len(dict_resultModels)

                    df_resultModels = pd.concat([df_resultModels, df_models], axis=0, ignore_index=True)

                    dict_resultModels[len(dict_resultModels)] = {
                         ModelNames.model1   : model1,
                         ModelNames.model2   : model2,
                         ModelNames.model3   : model3
                        }
        df_resultModels.to_csv('models.csv')
        bestModelId = self.findBestModelId(df_resultModels)
        best_resultModel = None if not bestModelId else dict_resultModels[bestModelId]
        return df_resultModels, dict_resultModels, best_resultModel

    def findBestModelId(self, df_resultModels):
        colV0PredCount = ModelNames.model1+ModelParameters.predictors_count
        colCH4PredCount = ModelNames.model2+ModelParameters.predictors_count
        colV0rmse = ModelNames.model1+ModelParameters.rmse
        colCH4rmse = ModelNames.model2+ModelParameters.rmse
        colV0r2 = ModelNames.model1+ModelParameters.adjusted_r_squared
        colCH4r2 = ModelNames.model2+ModelParameters.adjusted_r_squared
        colCH4LRr2 = ModelNames.model3+ModelParameters.adjusted_r_squared
        colCH4LRrmse = ModelNames.model3+ModelParameters.rmse
        df_conditions = df_resultModels.loc[(df_resultModels[colV0r2]>0.5) & (df_resultModels[colCH4r2]>0.5) & (df_resultModels[colCH4LRr2]>0.5)]
        df_sorted = df_conditions.sort_values(by=[colV0r2, colCH4r2, colCH4LRr2, colV0PredCount, colCH4PredCount, colV0rmse, colCH4rmse, colCH4LRrmse], ascending=[False, False, False, True, True, True, True, True], inplace=False, ignore_index = True)
        if not df_sorted is None or not df_sorted.emty:
            return df_sorted.loc[0, 'id']
        return None
    
    def modelToDataFrame(self, prefix, model : CalibrationModel):
        df = DataFrame(columns=
        [
         prefix + ModelParameters.function_name,
         prefix + ModelParameters.predictor_names,
         prefix + ModelParameters.predictors_count,
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
        df.at[0, prefix + ModelParameters.predictors_count] = model.predictors_count
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

        
    def generateTestDatasets(self, measuresCount = 44, func = lin_X, coefficients = [2, 0.5], step = 1):
        df_test = pd.DataFrame(columns=[
            ValuesNames.timestamp.getString(),
            ValuesNames.adc.getString(),
            ValuesNames.voltage.getString(),
            ValuesNames.temperature.getString(),
            ValuesNames.rHumidity.getString(),
            ValuesNames.aHumidity.getString(),
            ValuesNames.pressure.getString(),
            ValuesNames.ch4.getString()	
            ])
        t = dt.datetime.now()
        time = [t + dt.timedelta(seconds=i + round(random.random(), 2)) for i in range(measuresCount)]
        defaultADC = 50000
        defaultTemperature = 20
        defaultPressure = 100000
        defaultCH4 = 0
        minRH = 40
        maxRH = 100
        df_test[ValuesNames.timestamp.getString()] = time
        df_test[ValuesNames.adc.getString()] = [defaultADC] * measuresCount
        df_test[ValuesNames.voltage.getString()] = [defaultADC * 2.5 / 2**16] * measuresCount
        df_test[ValuesNames.temperature.getString()] = [defaultTemperature] * measuresCount
        df_test[ValuesNames.pressure.getString()] = [defaultPressure] * measuresCount
        df_test[ValuesNames.ch4.getString()] = [defaultCH4] * measuresCount
        if step == 1:
            temperature = list(np.linspace(0, 30, measuresCount))
            rh = random.sample(range(minRH, maxRH), measuresCount)
            aH = [self.absoluteHumidity(rh[i], defaultPressure, temperature[i]) for i in range(len(rh))]
            x_data = {ValuesNames.temperature.name : temperature, ValuesNames.aHumidity.name : aH, ValuesNames.rHumidity.name : rh}
            voltage0 = func(x_data, *coefficients)
            np.random.seed(1729)
            y_noise = 0.2 * np.random.normal(size=measuresCount)
            ydata = voltage0 + y_noise
            df_test[ValuesNames.voltage.getString()] = ydata
        #Второй шаг
        elif step == 2:
            temperature = [defaultTemperature] * measuresCount
            rh = random.sample(range(minRH, maxRH), measuresCount)
            aH = [self.absoluteHumidity(rh[i], defaultPressure, temperature[i]) for i in range(len(rh))]
            x_data = {ValuesNames.temperature.name : temperature, ValuesNames.aHumidity.name : aH, ValuesNames.rHumidity.name : rh}
            voltage0 = lin_X(x_data, *[2, 0.5])
            x_data[ValuesNames.voltage0.name] = voltage0
            df_test[ValuesNames.voltage0.getString()] = voltage0
            voltage = lin_X( {ValuesNames.rHumidity.name : rh}, *[4, 1])
            df_test[ValuesNames.voltage.getString()] = voltage
            x_data[ValuesNames.voltage.name] = voltage
            x_data[ValuesNames.rsr0.name] = RsR0_calc(x_data)
            df_test[ValuesNames.rsr0.getString()] = x_data[ValuesNames.rsr0.name]
            CH4 = ch4_lin_R_rH_T(x_data, *[0.5, 1, 2, -0.2])
            np.random.seed(500)
            y_noise = 0.2 * np.random.normal(size=measuresCount)
            CH4data = CH4 + y_noise
            df_test[ValuesNames.ch4Ref.getString()] = CH4data
            df_test[ValuesNames.ch4.getString()] = CH4

        df_test[ValuesNames.temperature.getString()] = list(temperature)
        df_test[ValuesNames.rHumidity.getString()] = rh
        df_test[ValuesNames.aHumidity.getString()] = aH
        

        df_test.to_csv('test_data.csv')

    def absoluteHumidity(self, RH, P, t):	
        Rv = 461.5 # J/(kg*K)
        ew = 6.112 * exp(17.62 * t / (243.12 + t)) * (1.0016 + 3.15e-6 * P - 0.074 / P) # Pa
        T = t + 273.15
        AH = RH * ew / Rv / T
        return AH
            

