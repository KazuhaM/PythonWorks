import os
import shutil
import pandas as pd
from tqdm import tqdm

oimage_f_pass = r"E:\Clouds\OneDrive - g.ecc.u-tokyo.ac.jp\LEP\2019\現行資料\0403モンゴル調査データ\Camera\DCIM\100OLYMP"
image_f_pass = r"E:\Clouds\OneDrive - g.ecc.u-tokyo.ac.jp\LEP\2020\00working\0901春期モンゴル解析6\ModImages"

Photolist_csv = pd.read_csv("Photolist.csv", sep=',')
imege_num = len(Photolist_csv)

for i_img in tqdm(range(imege_num)):
    ori_name = oimage_f_pass + "\\" + str(Photolist_csv["FileName"][i_img]) + ".jpg"

    if Photolist_csv["TypeNo"][i_img] == 1:
        re_name = image_f_pass + "\\Litter\\" + str(Photolist_csv["Rename"][i_img]) + ".jpg "
    elif Photolist_csv["TypeNo"][i_img] == 2:
        re_name = image_f_pass + "\\SpatialArrangement\\" + str(Photolist_csv["Rename"][i_img]) + ".jpg "
    elif Photolist_csv["TypeNo"][i_img] == 3:
        re_name = image_f_pass + "\\CenterPhoto\\" + str(Photolist_csv["Rename"][i_img]) + ".jpg "
    else:
        print("ERROR")
    
    shutil.copyfile(ori_name, re_name)
    # os.rename(ori_name, re_name) 
    