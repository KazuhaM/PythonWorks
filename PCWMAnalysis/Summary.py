#! python3
# Summary.py -　プログラム全体統合的実行

#######################使用ごとに変更するところ############################################
# 実行プログラム
run_func = [0,0,0,1]

# .pyファイルのあるフォルダ
# py_pass = r'D:\Documents\PythonWorks\PCWMAnalysis'
py_pass = r'C:\Users\Student\Documents\Pworks\PCWMAnalysis'
# データのあるフォルダ（作業フォルダ）（エクスプローラ上部passをそのままコピー）
# このフォルダの中に全csvファイルおよびデータの入ったサブフォルダを置く
# folder_pass = r"D:\OneDrive - g.ecc.u-tokyo.ac.jp\LEP\2019\現行資料\0802春季モンゴル解析2\OriginalData"
folder_pass = r"E:\Clouds\OneDrive - g.ecc.u-tokyo.ac.jp\LEP\2019\現行資料\0802春季モンゴル解析2\OriginalData"
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

avetime = [300]


# ## イベント分割用
# # イベント期間ファイル
event_csv = 'EventPeriod2.csv'

#######################関数本体###########################################################
### import
import pandas as pd
import os
import glob

# 他の関数の入った.pyをインポート
os.chdir(py_pass)
import timeadj
import reuexcep
import avebyn
import sepevent

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
    timeadj.timeadj(period_csv, wmdata_pass, pcdata_pass, timesep)

### 除外期間除去
if run_func[1] == 1:
    ## .\\avebynフォルダ内のファイルについて逐次実行
    # ファイル一覧取得
    timeadj_csvpass = os.path.join(folder_pass, 'timeadj', '*.csv')
    timeadj_flist = glob.glob(timeadj_csvpass)
    # timeadj_flist = timeadj_flist[1:3]
    # 各ファイルについて実行
    for itimeadj in timeadj_flist:
        ## 関数実行
        # 引数：ファイルの名前（itimeadj）, excep_csv, timesep
        # 出力データ： (csvファイル in .\excep)
        reuexcep.reuexcep(itimeadj, excep_csv, timesep)

### n秒間平均値算出
if run_func[2] == 1:
    ## .\excepフォルダ内のファイルについて逐次実行
    # ファイル一覧取得
    excep_csvpass = os.path.join(folder_pass, 'excep', '*.csv')
    excep_flist = glob.glob(excep_csvpass)
    for iavetime in avetime:
        # 各ファイルについて実行
        for iexcep in excep_flist:
            ## 関数実行
            # 引数：ファイルの名前（excep_flist）, avetime, timesep
            # 出力データ： (csvファイル in .\\avebyn)
            avebyn.avebyn(iexcep, iavetime, timesep)

### イベントでファイル分割
if run_func[3] == 1:
    ## .\avebynフォルダ内のファイルについて逐次実行
    # ファイル一覧取得
    # 各ファイルについて実行
        ## 関数実行
        # 引数：ファイルの名前, event_csv
        # 出力データ： (csvファイル in .\\sepevent)
    sepevent.sepevent(event_csv)