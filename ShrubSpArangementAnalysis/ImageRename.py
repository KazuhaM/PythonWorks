import os
import pandas as pd

oimage_f_pass = r"C:\Users\Student\Documents\Pworks\ShrubSpArangementAnalysis\OriImage"
image_f_pass = r"C:\Users\Student\Documents\Pworks\ShrubSpArangementAnalysis\SpAraImage"

Photolist_csv = pd.read_csv("Photolist.csv", sep=',')
imege_num = len(Photolist_csv)

for i_img in range(imege_num):
    ori_name = oimage_f_pass + "\\P" + str(Photolist_csv["FileName"][i_img]) + ".jpg"
    re_name = image_f_pass + "\\" +str(Photolist_csv["rename"][i_img]) + ".jpg"
    
    os.rename(ori_name, re_name)