#! python3
# sepevent.py -　サイトごとの時刻合わせデータ作成

# package import
import pandas as pd
import os
import numexpr
## 関数実行
# 引数：ファイルの名前, event_csv
# 出力データ： (csvファイル in .\\sepevent)
def sepevent(p_event_csv):
    eventf_csv = pd.read_csv(p_event_csv, sep=',')
    eventf_csv["Start"] = pd.to_datetime(eventf_csv["Start"], format=r'%Y-%m-%d %H:%M')
    eventf_csv["End"] = pd.to_datetime(eventf_csv["End"], format=r'%Y-%m-%d %H:%M')
    nevent = len(eventf_csv)

    sumdata = pd.read_csv("sumdata.csv", sep=',')
    sumdata["Time"] = pd.to_datetime(sumdata["Time"], format=r'%Y-%m-%d %H:%M:%S')
    sumdata["Event"] = 99

    for ievent in range(nevent):
        # 各イベントの最初と最後を取得
        # イベント名を取得
        iEventID = eventf_csv["Event"][ievent]
        iStart = eventf_csv["Start"][ievent]
        iEnd = eventf_csv["End"][ievent]
        for irow in range(len(sumdata)):
            if iStart <= sumdata["Time"][irow] and sumdata["Time"][irow] <= iEnd:
                sumdata.iat[irow,2] = iEventID

    out_filename = 'Ev_sumdata.csv'
    sumdata.to_csv(out_filename, index = False)
