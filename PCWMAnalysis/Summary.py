#! python3
# Summary.py -　プログラム全体の流れ記述（最後の統合的実行もありか）

#######################使用ごとに変更するところ############################################
### パラメータ一覧
# データのあるフォルダ（作業フォルダ）
folder_pass = "c:\\Users\\Student\\Documents\\Pworks\\PCWMAnalysis/"
# サイトごとの観測期間ファイル
period_csv = 'SitePeriod.csv'

## 時刻合わせ関数用
# WMデータファイルが入ったフォルダpass
wmdata_pass = r"E:\Clouds\OneDrive - g.ecc.u-tokyo.ac.jp\LEP\2019\現行資料\0802春季モンゴル解析2\OriginalData\ModifiedKestrel"
# PCデータファイルが入ったフォルダpass
pcdata_pass = r"E:\Clouds\OneDrive - g.ecc.u-tokyo.ac.jp\LEP\2019\現行資料\0802春季モンゴル解析2\OriginalData\ModifiedPC"
# 時刻間隔（s）
timesep = 10

## n秒間平均値算出用
# 何秒で平均を取るか
avetime = 60 * 5


########################関数本体#########################################################
### import
import pandas as pd
import os
### 準備
# 作業フォルダ変更
os.getcwd()
os.chdir(folder_pass)
# サイトごとの観測期間csvファイル読み込み
siteperiod_csv = pd.read_csv(period_csv, sep=',')
# 日時列をdatetime形式に
siteperiod_csv["Start"] = pd.to_datetime(siteperiod_csv["Start"], format=r'%Y/%m/%d %H:%M')
siteperiod_csv["End"] = pd.to_datetime(siteperiod_csv["End"], format=r'%Y/%m/%d %H:%M')

### 全サイトで処理をまとめて行う
siteperiod_index = len(siteperiod_csv.index)

for iSite in range(siteperiod_index):
## 各行のデータを一時変数に渡して、各処理を行う関数に渡す
# 要作成データ：SiteID, IDNo, Type, Height, Start, End,
    iSiteID = siteperiod_csv["SiteID"][iSite]
    iIDNo = siteperiod_csv["IDNo"][iSite]
    iType = siteperiod_csv["Type"][iSite]
    iHeight = siteperiod_csv["Height"][iSite]
    iStart = siteperiod_csv["Start"][iSite]
    iEnd = siteperiod_csv["End"][iSite]

## サイトごとの時刻合わせデータ作成
# 入力変数： iSiteID, iIDNo, iType, iHeight, iStart, iEnd, wmdata_pass, pcdata_pass, timesep
# 出力データ： (csvファイル in .\\tajst)


## n秒間平均値算出
# 入力変数：SiteID, IDNo, Type, Height, Start, End

## 除外期間除去
# 入力変数：SiteID, IDNo, Type, Height, Start, End

## イベントでファイル分割
# 入力変数：SiteID, IDNo, Type, Height, Start, End