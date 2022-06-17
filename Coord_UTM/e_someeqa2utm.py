import f_eqa2utm
import pandas as pd

# read csv
dataFolder = "C:/Users/niedo/OneDrive/SL/2022/202206モンゴル調査/PreliminaryStudy/GPX"
data_csv = pd.read_csv(dataFolder + "/Grid240_ponits_coordinate.csv")

# make blank data frame for the result
cols = ['x', 'y']
result_df = pd.DataFrame(index=[], columns=cols)

for row in data_csv.itertuples():
    # print(row.y)
    utm_result = f_eqa2utm.eqa2Utm(lon=row.y, lat=row.x, zone = False) 
    
    utm_record = pd.DataFrame({'x': utm_result[1], 'y': utm_result[0]},  index = ['1'])
    # print(utm_record)
    result_df = pd.concat([result_df, utm_record], ignore_index=True)

# print(data_csv)
# utm_result = utm2eqa.utm2Epa(lon=105.93856674505157, lat=46.88053214466702) #[deg.]
# print(result_df)
result_df.to_csv(dataFolder + '/Grid240_ponits_coordinateUTM.csv',index=False)