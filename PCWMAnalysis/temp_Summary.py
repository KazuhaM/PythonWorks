#! python3
# Summary.py -　プログラム全体統合的実行

# 温度、相対湿度用コード
#######################使用ごとに変更するところ############################################
# 実行プログラム
# run_func = [0,0,1,0]
run_func = [0,0,0,1]
# run_func = [0,1,1,0]
# run_func = [0,1,0,0]
# run_func = [0,1,1,0]
# .pyファイルのあるフォルダ
py_pass = r'D:\Documents\Pworks\PCWMAnalysis'
# py_pass = r'C:\Users\Student\Documents\Pworks\PCWMAnalysis'
# データのあるフォルダ（作業フォルダ）（エクスプローラ上部passをそのままコピー）
# このフォルダの中に全csvファイルおよびデータの入ったサブフォルダを置く
folder_pass = r"D:\OneDrive - g.ecc.u-tokyo.ac.jp\LEP\2019\現行資料\0802春季モンゴル解析2\OriginalData"
# folder_pass = r"E:\Clouds\OneDrive - g.ecc.u-tokyo.ac.jp\LEP\2019\現行資料\0802春季モンゴル解析2\OriginalData"
# サイトごとの観測期間ファイル
period_csv = 'SitePeriod.csv'

## 時刻合わせ関数用
# WMデータファイルが入ったフォルダ名
wmdata_pass = "ModWM"

# PCデータファイルが入ったフォルダpass
pcdata_pass = "ModPC"

# 時刻間隔（s）（PC, WMの測定間隔の最大公約数）
timesep = 10

## 除外期間除去
# 除去期間ファイル
excep_csv = 'ExceptionPeriod.csv'

## n秒間平均値算出用
# 何秒で平均を取るか

avetime = [60, 180, 300, 600, 1800 ]


# ## イベント分割用
# # イベント期間ファイル
event_csv = 'EventPeriod.csv'

#######################関数本体###########################################################
### import
import pandas as pd
import os
import glob
# import pyper

# 他の関数の入った.pyをインポート
os.chdir(py_pass)
import temp_timeadj
import temp_reuexcep
import temp_avebyn
import temp_sepevent

### 準備
# 作業フォルダ変更
os.chdir(folder_pass)

# ファイルpassを絶対パスに
period_csv = os.path.join(folder_pass, period_csv)
wmdata_pass = os.path.join(folder_pass, wmdata_pass)
pcdata_pass = os.path.join(folder_pass, pcdata_pass)
excep_csv = os.path.join(folder_pass, excep_csv)
event_csv = os.path.join(folder_pass, event_csv)

### サイトごとの時刻合わせデータ作成
if run_func[0] == 1:
    # 引数：period_csv, wmdata_pass, pcdata_pass, timesep
    # 出力データ： (csvファイル in .\timeadj)
    temp_timeadj.timeadj(period_csv, wmdata_pass, pcdata_pass, timesep)

### 除外期間除去
if run_func[1] == 1:
    ## .\\avebynフォルダ内のファイルについて逐次実行
    # ファイル一覧取得
    timeadj_csvpass = os.path.join(folder_pass, 'temp_timeadj', '*.csv')
    timeadj_flist = glob.glob(timeadj_csvpass)
    # timeadj_flist = timeadj_flist[1:3]
    # 各ファイルについて実行
    for itimeadj in timeadj_flist:
        ## 関数実行
        # 引数：ファイルの名前（itimeadj）, excep_csv, timesep
        # 出力データ： (csvファイル in .\excep)
        temp_reuexcep.reuexcep(itimeadj, excep_csv, timesep)

### n秒間平均値算出
if run_func[2] == 1:
    ## .\excepフォルダ内のファイルについて逐次実行
    # ファイル一覧取得
    excep_csvpass = os.path.join(folder_pass, 'temp_excep', '*.csv')
    excep_flist = glob.glob(excep_csvpass)
    for iavetime in avetime:
        # 各ファイルについて実行
        for iexcep in excep_flist:
            ## 関数実行
            # 引数：ファイルの名前（excep_flist）, avetime, timesep
            # 出力データ： (csvファイル in .\\avebyn)
            temp_avebyn.avebyn(iexcep, iavetime, timesep)

# ###時系列グラフ、平均値ごとの全サイト統合データ作成
# r = pyper.R()
# r(r"setwd('C:/Users/Student/Documents/Pworks/PCWMAnalysis'); source(file='MergeData_PlotSummary.r',encoding='utf-8')")

### イベント情報代入
if run_func[3] == 1:
    ## .\avebynフォルダ内のファイルについて逐次実行
    # ファイル一覧取得
    # 各ファイルについて実行
        ## 関数実行
        # 引数：ファイルの名前, event_csv
        # 出力データ： (csvファイル in .\\sepevent)
    for isec in range(len(avetime)):
        sumdata_pass = 'temp'+ str(avetime[isec]) + '_sumdata.csv'
        temp_sepevent.sepevent(event_csv, sumdata_pass)