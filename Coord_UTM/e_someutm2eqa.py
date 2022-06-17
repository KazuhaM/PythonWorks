import f_utm2eqa
import pandas as pd
from tqdm import tqdm

# read csv
dataFolder = "C:/Users/niedo/OneDrive/SL/2022/202206モンゴル調査/PreliminaryStudy/GPX"
data_csv = pd.read_csv(dataFolder + "/quad_coordinateUTM.csv")

# make blank data frame for the result
cols = ['lon', 'lat','name','sym']
result_df = pd.DataFrame(index=[], columns=cols)

with tqdm(total=len(data_csv)) as pbar:
    for row in tqdm(data_csv.itertuples()):
        # print(row.y)
        utm_result = f_utm2eqa.utm2Eqa(utmx=row.lon, utmy=row.lat, zone = 48) 
        
        utm_record = pd.DataFrame({'lon': utm_result[0], 'lat': utm_result[1], 'name': row.name, 'sym': row.sym},  index = ['1'])
        # print(utm_record)
        result_df = pd.concat([result_df, utm_record], ignore_index=True)
        pbar.update(1)

# print(data_csv)
# utm_result = utm2eqa.utm2Epa(lon=105.93856674505157, lat=46.88053214466702) #[deg.]
# print(result_df)
result_df.to_csv(dataFolder + '/quad_coordinate.csv',index=False)