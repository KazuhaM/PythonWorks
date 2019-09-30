#! python3
# timeadj.py -　サイトごとの時刻合わせデータ作成

# package import
import pandas as pd
import datetime as dt
import numpy as np
from datetime import timedelta
import glob

def timeadj(p_period_csv, p_wmdata_pass, p_pcdata_pass, p_timesep):
    siteperiod_csv = pd.read_csv(p_period_csv, sep=',')
    # 日時列をdatetime形式に
    siteperiod_csv["Start"] = pd.to_datetime(siteperiod_csv["Start"], format=r'%Y/%m/%d %H:%M')
    siteperiod_csv["End"] = pd.to_datetime(siteperiod_csv["End"], format=r'%Y/%m/%d %H:%M')

    ### サイトごとの時刻合わせデータ作成
    ## siteperiod_csvの各行について実行。
                                                            # uniSiteID = siteperiod_csv["SiteID"].unique()
    siteperiod_num = len(siteperiod_csv.index)    # 一時変数に入れておく
    for iSite in range(2, siteperiod_num + 2):
        # サイト期間ファイルの2行目から順に見ていく
        ## 各行のデータを一時変数に渡して、各処理を行う関数に渡す
        # 要作成データ：SiteID, IDNo, Type, Height, Start, End,
        iSiteID = siteperiod_csv["SiteID"][iSite]
        iIDNo = siteperiod_csv["IDNo"][iSite]
        iType = siteperiod_csv["Type"][iSite]
        iHeight = siteperiod_csv["Height"][iSite]
        iStart = siteperiod_csv["Start"][iSite]
        iEnd = siteperiod_csv["End"][iSite]

        sec_num = int((iEnd - iStart).total_seconds() + 1)
        timelist = [iStart + timedelta(seconds = x) for x in range(0, sec_num, p_timesep)]
        # PCかWMかを判定して処理を変える（閲覧するフォルダ、データ挿入用列の数）
        try:
            if iType == 'PC':
                # StartとEndから作った一連の時刻の列と、それと同じ行数を持つ空の値を持つ列（データ挿入用）を持つデータフレーム（pd.DataFrame）を作る
                colname = 'PC' + str(iIDNo) +'_' + str(iHeight)
                sumajdata = pd.DataFrame({'Time': timelist})
                # sumajdata[colname] = np.nan

                # データファイルの一覧リスト取得
                datafd = os.path.join(p_pcdata_pass, '*.csv')
                dataflst = glob.glob(datafd)

                # データファイルごとに処理
                for iDataf in range(len(dataflst)):
                    # 　条件に該当するデータファイルを取得
                    Dataf_day = os.path.basename(dataflst[iDataf])
                    Dataf_day = Dataf_day.replace('.csv', '')
                    Dataf_day = pd.to_datetime(Dataf_day, format='%y%m%d')
                    if timecomp(iStart, Dataf_day, "day", "<=") and timecomp(Dataf_day, iEnd, "day", "<="):
                        tmpPC_csv = pd.read_csv(dataflst[iDataf], sep=',')
                        tmpPC_csv = tmpPC_csv.rename(columns={tmpPC_csv.columns[0]: 'Time'})
                        tmpPC_csv["Time"] = pd.to_datetime(tmpPC_csv["Time"], format=r'%Y/%m/%d %H:%M')
                        # 秒が消えてないか判定

                        # 時系列とその時の該当iIDNoのデータを切り出して、sumajdataにマージ
                        if "LR5061-" + str(iIDNo) in list(tmpPC_csv.columns):
                            tmpPC_csv=tmpPC_csv.loc[:,[tmpPC_csv.columns[0],"LR5061-" + str(iIDNo)]]
                            sumajdata = pd.merge(sumajdata, tmpPC_csv, left_on='Time', right_on=tmpPC_csv.columns[0], how='left')
                            sumajdata = sumajdata.rename(columns={"LR5061-" + str(iIDNo): colname})
            elif iType == 'WM':
                colname = ['WS' + '_' + str(iHeight),'WD' + '_' + str(iHeight)]
                sumajdata = pd.DataFrame({'Time': timelist})
                sumajdata[colname[0]] = np.nan
                sumajdata[colname[1]] = np.nan
            else:
                raise Exception('siteperiod_csvのTypeに不正な形式があります。' + str(iSite) + '行目')
        except Exception as err:
            print('ERROR: ' + str(err))

        
        # 開くべきデータファイルの一覧を取得する
        # データファイルを一つずつ開く
        # データファイル2行目について、データフレームの時刻列に存在するか確認する
        # 存在したら該当する時刻のデータフレームの行のデータ挿入用列に必要なデータを上書きする
        # 存在しなければデータフレームの次の行を見て同様にする
        # 一度存在したら、次のデータファイル行をデータフレームの次の行に挿入していく
        # その際、時刻の同一性を必ず確認し、同一でなければさらに次のデータフレームの行をトライする
        # データファイルの最終行まで行ったらデータフレームをシェルフファイルに保存し（開いて代入して閉じる）次の開くべきデータファイルに移行する
        # 開くべきデータファイルがすべて検証し終わったらサイト期間ファイルの次の行に移行する
        # SiteIDが次の行で変わるなら、シェルフファイルを開いてマージ処理をする（pd.DataFrame.merge(), pd.merge(データフレーム1, データフレーム2, on='統合のキーに使う列名', how='outer'))）
        # シェルフファイルを初期化する

    

        ## サイトごとの時刻合わせデータ作成
        # 引数： iSiteID, iIDNo, iType, iHeight, iStart, iEnd, wmdata_pass, pcdata_pass, timesep
        # 出力データ： (csvファイル in .\timeadj)
        timeadj.timeadj(iSiteID, iIDNo, iType, iHeight, iStart, iEnd, wmdata_pass, \
            pcdata_pass, timesep)

def timecomp(time1, time2, revel="second", comptype="=="):
    revlist = ["year", "month", "day", "hour", "minute", "second"]
    if comptype == "==":
        ysame = time1.year == time2.year
        msame = time1.month == time2.month
        dsame = time1.day== time2.day
        hsame = time1.hour == time2.hour
        misame = time1.minute == time2.minute
        ssame = time1.second == time2.second
    elif comptype == ">=":
        ysame = time1.year >= time2.year
        msame = time1.month >= time2.month
        dsame = time1.day>= time2.day
        hsame = time1.hour >= time2.hour
        misame = time1.minute >= time2.minute
        ssame = time1.second >= time2.second
    elif comptype == "<=":
        ysame = time1.year <= time2.year
        msame = time1.month <= time2.month
        dsame = time1.day<= time2.day
        hsame = time1.hour <= time2.hour
        misame = time1.minute <= time2.minute
        ssame = time1.second <= time2.second
    elif comptype == "<":
        ysame = time1.year < time2.year
        msame = time1.month < time2.month
        dsame = time1.day< time2.day
        hsame = time1.hour < time2.hour
        misame = time1.minute < time2.minute
        ssame = time1.second < time2.second
    elif comptype == ">":
        ysame = time1.year > time2.year
        msame = time1.month > time2.month
        dsame = time1.day> time2.day
        hsame = time1.hour > time2.hour
        misame = time1.minute > time2.minute
        ssame = time1.second > time2.second
    elif comptype == "!=":
        ysame = time1.year != time2.year
        msame = time1.month != time2.month
        dsame = time1.day!= time2.day
        hsame = time1.hour != time2.hour
        misame = time1.minute != time2.minute
        ssame = time1.second != time2.second

    if revel in revlist[0:len(revlist)]:
        sametime = ysame
    if revel in revlist[1:len(revlist)]:
        sametime = sametime and msame
    if revel in revlist[2:len(revlist)]:
        sametime = sametime and dsame
    if revel in revlist[3:len(revlist)]:
        sametime = sametime and hsame
    if revel in revlist[4:len(revlist)]:
        sametime = sametime and misame
    if revel in revlist[5:len(revlist)]:
        sametime = sametime and ssame
    return sametime

def secheck(times=6):
    