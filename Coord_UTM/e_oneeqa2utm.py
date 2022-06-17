import f_eqa2utm
import pandas as pd

# read csv
dataFolder = "C:/Users/niedo/OneDrive/SL/2022/202206MongoliaSurvey/PreliminaryStudy/GPX"
data_csv = pd.read_csv(dataFolder + "/RefPoint.csv")
# print(data_csv)

utm_result = f_eqa2utm.eqa2Utm(lon=data_csv.at[0, 'lon'], lat=data_csv.at[0,'lat']) #[deg.]
utm_result = pd.DataFrame({'x': utm_result[2], 'y': utm_result[1]}, index = ['1'])
# print(utm_result)
utm_result.to_csv(dataFolder + '/RefPointUTM.csv',index=False)