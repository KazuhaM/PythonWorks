#! python3
# Summary.py -　プログラム全体統合的実行

#######################使用ごとに変更するところ############################################
# データのあるフォルダ（作業フォルダ）（エクスプローラ上部passをそのままコピー）
# このフォルダの中に全csvファイルおよびデータの入ったサブフォルダを置く
folder_pass = r"E:\Clouds\OneDrive - g.ecc.u-tokyo.ac.jp\LEP\2019\現行資料\0802春季モンゴル解析2\OriginalData"
# サイトごとの観測期間ファイル
period_csv = 'SitePeriod.csv'

## 時刻合わせ関数用
# WMデータファイルが入ったフォルダ名
wmdata_pass = "ModifiedKestrel"

# PCデータファイルが入ったフォルダpass
pcdata_pass = "ModifiedPC"

# 時刻間隔（s）（PC, WMの測定間隔の最大公約数）
timesep = 10

## 除外期間除去
# 除去期間ファイル
excep_csv = 'ExceptionPeriod.csv'

## n秒間平均値算出用
# 何秒で平均を取るか
avetime = 60 * 5

## イベント分割用
# イベント期間ファイル
event_csv = 'EventPeriod.csv'

#######################関数本体###########################################################
### import
import pandas as pd
import os
import glob

import timeadj
import reuexcep
import avebyn


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
# 引数：period_csv, wmdata_pass, pcdata_pass, timesep
# 出力データ： (csvファイル in .\timeadj)
timeadj.timeadj(period_csv, wmdata_pass, pcdata_pass, timesep)

### 除外期間除去
## .\\avebynフォルダ内のファイルについて逐次実行
# ファイル一覧取得
timeadj_csvpass = os.path.join(folder_pass, 'timeadj', '*.csv')
timeadj_flist = glob.glob(timeadj_csvpass)
# 各ファイルについて実行
for itimeadj in timeadj_flist
    ## 関数実行
    # 引数：ファイルの名前（itimeadj）, excep_csv
    # 出力データ： (csvファイル in .\excep)
    reuexcep.reuexcep(itimeadj, excep_csv)

### n秒間平均値算出
## .\excepフォルダ内のファイルについて逐次実行
# ファイル一覧取得
excep_csvpass = os.path.join(folder_pass, 'excep', '*.csv')
excep_flist = glob.glob(excep_csvpass)
# 各ファイルについて実行
for iexcep in excep_flist
    ## 関数実行
    # 引数：ファイルの名前（excep_flist）, avetime
    # 出力データ： (csvファイル in .\\avebyn)
    avebyn.avebyn(iexcep, avetime)

### イベントでファイル分割
## .\avebynフォルダ内のファイルについて逐次実行
# ファイル一覧取得
# 各ファイルについて実行
    ## 関数実行
    # 引数：ファイルの名前, event_csv
    # 出力データ： (csvファイル in .\\sepevent)