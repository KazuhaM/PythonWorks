import numpy as np
import pandas as pd
import cv2
from matplotlib import pyplot as plt
from tqdm import tqdm

# フォルダパス
# image_f_pass = r"C:\Users\Student\Documents\Pworks\ShrubSpArangementAnalysis\SpAraImage"
image_f_pass = r"D:\Documents\Pworks\ShrubSpArangementAnalysis\SpAraImage"

# image_f_pass = r"E:\Clouds\OneDrive - g.ecc.u-tokyo.ac.jp\LEP\2020\00working\0901春期モンゴル解析6\ModImages\SpatialArrangement"
# image_f_pass = r"D:\OneDrive - g.ecc.u-tokyo.ac.jp\LEP\2020\00working\0901春期モンゴル解析6\ModImages\SpatialArrangement"

# output_f_pass = r"E:\Clouds\OneDrive - g.ecc.u-tokyo.ac.jp\LEP\2020\00working\0901春期モンゴル解析6\ModImages\SpatialArrangement\ProjectiveTrans"
# output_f_pass = r"D:\OneDrive - g.ecc.u-tokyo.ac.jp\LEP\2020\00working\0901春期モンゴル解析6\ModImages\SpatialArrangement\ProjectiveTrans"
output_f_pass = r"D:\Documents\Pworks\ShrubSpArangementAnalysis\ProjectiveTrans"



# アウトプット画像の一辺のサイズ（正方形）
sq_len = 2700
## 正方形の画像に修正
p_trans = np.float32([[0, 0], [sq_len, 0], [0, sq_len], [sq_len, sq_len]])
print(p_trans)
# print(type(p_trans))

# ImageJから取得した四方の座標CSVを読み込み
Coordinate_csv = pd.read_csv("QuadPosition.csv", sep=',')
# ImageJの結果CSVから画像の種類を取得（indexとか、、、）
ImegeArry = Coordinate_csv['Label'].unique()
# 繰り返し
imege_num = len(ImegeArry)
for i_img in tqdm(range(imege_num)):
    # SpAraImageフォルダから、同名の画像を読み込む
    i_img_name = ImegeArry[i_img]
    i_img_pass = image_f_pass + "\\" + i_img_name # + ".jpg"
    
    print(i_img_pass)
    i_img_img = cv2.imread(i_img_pass, 1)  # 画像読み込み
    print(i_img_img.shape)
    
    # 変換前後の対応点を設定
    # その画像の四方の座標を読み込み取得
    ## 座標格納配列を初期化
    p_original = np.float32([[0,0], [0,0], [0,0], [0,0]])
    for i_cor in range(4):
        p_original[i_cor] = Coordinate_csv.loc[i_img * 4 + i_cor, ['X','Y']]
    
    print(i_img_name)
    # print(p_original)
    # print(type(p_original))
    # 射影変換
    ## 変換マトリクスと射影変換
    transMat = cv2.getPerspectiveTransform(p_original, p_trans)
    i_img_trans = cv2.warpPerspective(i_img_img, transMat, (sq_len, sq_len))
    
    ## 変換画像をProjectiveTransフォルダに保存
    i_output_pass = output_f_pass + "\\" + i_img_name + ".jpg"
    cv2.imwrite(i_output_pass, i_img_trans)

    # #ここからグラフ設定
    # fig = plt.figure()
    # ax1 = fig.add_subplot(111)
    
    # # 画像をプロット
    # show = cv2.cvtColor(i_trans, cv2.COLOR_BGR2RGB)
    # ax1.imshow(show)
    
    # fig.tight_layout()
    # plt.show()
    # plt.close()