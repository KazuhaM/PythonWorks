#! python3
# reuexcep.py -　サイトごとの時刻合わせデータ作成

# package import
import pandas as pd
import os
from datetime import timedelta

# 引数：ファイルの名前（itimeadj）, excep_csv
# 出力データ： (csvファイル in .\excep)
def reuexcep(p_itimeadj, p_excep_csv, p_timesep):
    ## ファイル展開
    # 対象ファイルを開く
    dataf_csv = pd.read_csv(p_itimeadj, sep=',')
    # 日時列をdatetime形式に
    dataf_csv["Time"] = pd.to_datetime(dataf_csv["Time"], format=r'%Y-%m-%d %H:%M:%S')
    # ファイル名からサイトID取得
    SiteID = os.path.basename(p_itimeadj)
    SiteID = SiteID.replace('TiAd_', '')
    SiteID = SiteID.replace('.csv', '')

    # 除去期間ファイルを開く
    excepf_csv = pd.read_csv(p_excep_csv, sep=',')
    # 日時列をdatetime形式に
    excepf_csv["Start"] = pd.to_datetime(excepf_csv["Start"], format=r'%Y/%m/%d %H:%M')
    excepf_csv["End"] = pd.to_datetime(excepf_csv["End"], format=r'%Y/%m/%d %H:%M')
    len_excep = len(excepf_csv)

    ## 対象ファイルについて、除去期間に記載の全除去期間を探査する
    for excep_row in range(len_excep):
        if excepf_csv.iat[excep_row,0] in SiteID:
            # 終了時刻のみ（この時刻以前は除去）
            if excepf_csv.iat[excep_row,1] == 1:
                # 時刻列をリストとして取得して、その中から該当する時刻を探索
                if excepf_csv.iat[excep_row,3] in list(dataf_csv["Time"]):
                    slend = list(dataf_csv["Time"]).index(excepf_csv.iat[excep_row,3])
                dataf_csv = dataf_csv[slend:]
            # 開始時刻のみ（この時刻以降は除去）
            elif excepf_csv.iat[excep_row,4] == 1:
                # 時刻列をリストとして取得して、その中から該当する時刻を探索
                if excepf_csv.iat[excep_row,2] in list(dataf_csv["Time"]):
                    slstart = list(dataf_csv["Time"]).index(excepf_csv.iat[excep_row,2])
                dataf_csv = dataf_csv[:slstart]
            # 期間（この期間は除去）
            else:
                # 時刻列をリストとして取得して、その中から該当する時刻を探索
                if excepf_csv.iat[excep_row,2] in list(dataf_csv["Time"]):
                    slstart = list(dataf_csv["Time"]).index(excepf_csv.iat[excep_row,2])
                else:
                    if excepf_csv.iat[excep_row,2] <= dataf_csv.iat[0,0]:
                        slstart = 0
                    else:
                        continue
                if excepf_csv.iat[excep_row,3] in list(dataf_csv["Time"]):
                    slend = list(dataf_csv["Time"]).index(excepf_csv.iat[excep_row,3])
                else:
                    if dataf_csv.iat[len(dataf_csv) - 1,0] <= excepf_csv.iat[excep_row,3]:
                        slend = len(dataf_csv) - 1
                    else:
                        continue
                dataf_csv = dataf_csv.drop(dataf_csv.index[list(range(slstart,slend+1))])
        # print(excep_row)
    if not os.path.exists('.\\excep'):
       os.makedirs('.\\excep')
    out_filename = 'Ex_' + SiteID + '.csv'
    dataf_csv.to_csv('.\\excep\\' + out_filename, index = False)
    print("reuexcep: " + SiteID + "まで終了")






