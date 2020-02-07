#! python3
# timeadj.py -　サイトごとの時刻合わせデータ作成

# package import
import pandas as pd
import datetime as dt
import numpy as np
from datetime import timedelta
import os
import shutil
import glob
import shelve
import math
import re

def timeadj(p_period_csv, p_wmdata_pass, p_pcdata_pass, p_timesep):
    # 変数一時保管ファイルの居場所を作る
    tmp_pass = os.path.join(os.getcwd(), 'tmp')
    os.makedirs(tmp_pass)

    # サイトの開始・終了日時を書いたファイルを開く
    siteperiod_csv = pd.read_csv(p_period_csv, sep=',')
    # 日時列をdatetime形式に
    siteperiod_csv["Start"] = pd.to_datetime(siteperiod_csv["Start"], format=r'%Y/%m/%d %H:%M')
    siteperiod_csv["End"] = pd.to_datetime(siteperiod_csv["End"], format=r'%Y/%m/%d %H:%M')

    ### サイトごとの時刻合わせデータ作成
    ## siteperiod_csvの各行について実行。
                                                            # uniSiteID = siteperiod_csv["SiteID"].unique()
    siteperiod_num = len(siteperiod_csv.index)    # 一時変数に入れておく
    for iSite in range(siteperiod_num):
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
                    # print(iDataf)
                    # ファイルを開く
                    tmpPC_csv = pd.read_csv(dataflst[iDataf], sep=',')
                    tmpPC_csv = tmpPC_csv.rename(columns={tmpPC_csv.columns[0]: 'Time'})
                    tmpPC_csv["Time"] = pd.to_datetime(tmpPC_csv["Time"], format=r'%Y/%m/%d %H:%M:%S')
                    # 最初と最後の時刻を取る
                    fStart = tmpPC_csv.iat[0,0]
                    fend = tmpPC_csv.iat[len(tmpPC_csv["Time"])-1,0]
                    PCidinList = [s for s in list(tmpPC_csv.columns) if re.match('^LR5061-(0)*' + str(iIDNo) + '$', s)]
                    if not fend <= iStart and\
                         not iEnd <= fStart and\
                         len(PCidinList) == 1:
                        # 秒が消えてないか判定（最初の三行で秒が00のままなら秒データが消えていると判定して再生成）
                        if tmpPC_csv.iat[0,0].second == 0 and \
                            tmpPC_csv.iat[1,0].second == 0 and \
                            tmpPC_csv.iat[2,0].second == 0:
                            print('iSite:'+ str(iSite)+', iDataf:'+ str(iDataf)+', iIDNo:'+ str(iIDNo))
                            modsec(tmpPC_csv)

                        # 時系列とその時の該当iIDNoのデータを切り出して、sumajdataにマージ
                        tmpPC_csv=tmpPC_csv.loc[:,[tmpPC_csv.columns[0],PCidinList[0]]]
                        sumajdata_test = pd.merge(sumajdata, tmpPC_csv, left_on='Time', right_on=tmpPC_csv.columns[0], how='left')
                        if not sumajdata_test[PCidinList[0]].isnull().all():
                            sumajdata = pd.merge(sumajdata, tmpPC_csv, left_on='Time', right_on=tmpPC_csv.columns[0], how='left')
                            if len(sumajdata.columns) != 2:
                                if sumajdata.iloc[:, 1].isnull().any():
                                    boolnullist = list(sumajdata.iloc[:, 1].isnull())
                                    for isumr in range(len(boolnullist)):
                                        if boolnullist[isumr]:
                                            sumajdata.iloc[isumr, 1] = sumajdata.iloc[isumr, 2]
                                    del sumajdata[PCidinList[0]]
                            else:
                                sumajdata = sumajdata.rename(columns={PCidinList[0]: colname})
                # 作成したsumajdataをシェルフファイルに保存
                shelf_file = shelve.open('./tmp/tempdata')
                while colname in list(shelf_file.keys()):
                    colname = colname + '_2'
                shelf_file[colname] = sumajdata
                shelf_file.close()
            elif iType == 'WM':
                # StartとEndから作った一連の時刻の列と、それと同じ行数を持つ空の値を持つ列（データ挿入用）を持つデータフレーム（pd.DataFrame）を作る
                colname = 'WM' + str(iIDNo) +'_' + str(iHeight)
                sumajdata = pd.DataFrame({'Time': timelist})
                # sumajdata[colname] = np.nan

                # データファイルの一覧リスト取得
                datafd = os.path.join(p_wmdata_pass, 'WEATHER - *.csv')
                dataflst = glob.glob(datafd)

                # データファイルごとに処理
                for iDataf in range(len(dataflst)):
                    # 　条件に該当するデータファイルを取得
                    Dataf_day = os.path.basename(dataflst[iDataf])
                    Dataf_day = Dataf_day.replace('WEATHER - ', '')
                    Dataf_day = Dataf_day.replace('.csv', '')
                    Dataf_day = Dataf_day.split('_')[0]

                    # ファイルを開く
                    tmpWM_csv = pd.read_csv(dataflst[iDataf], sep=',')
                    tmpWM_csv = tmpWM_csv.rename(columns={tmpWM_csv.columns[0]: 'Time'})
                    tmpWM_csv["Time"] = pd.to_datetime(tmpWM_csv["Time"], format=r'%Y-%m-%d %H:%M:%S')
                    # 最初と最後の時刻を取る
                    fStart = tmpWM_csv.iat[0,0]
                    fend = tmpWM_csv.iat[len(tmpWM_csv["Time"])-1,0]
                    # 時刻が適切でかつ測器番号が今調べているIDと合致するか
                    if not fend <= iStart and\
                         not iEnd <= fStart and\
                         Dataf_day == str(iIDNo):
                        # 秒が消えてないか判定（最初の三行で秒が00のままなら秒データが消えていると判定して再生成）
                        if tmpWM_csv.iat[0,0].second == 0 and \
                            tmpWM_csv.iat[1,0].second == 0 and \
                            tmpWM_csv.iat[2,0].second == 0:
                            print('iSite:'+ str(iSite)+', iDataf:'+ str(iDataf)+', iIDNo:'+ str(iIDNo))
                            modsec(tmpWM_csv)
                        # 時系列とその時の該当iIDNoのデータを切り出して、sumajdataにマージ
                        tmpWM_csv=tmpWM_csv.loc[:,["Time","Temp","Rel. Hum."]]
                        sumajdata_test = pd.merge(sumajdata, tmpWM_csv, left_on='Time', right_on=tmpWM_csv.columns[0], how='left')
                        if not sumajdata_test["Temp"].isnull().all():
                            sumajdata = pd.merge(sumajdata, tmpWM_csv, left_on='Time', right_on=tmpWM_csv.columns[0], how='left')
                            if len(sumajdata.columns) != 3:
                                if sumajdata.iloc[:, 1].isnull().any():
                                    boolnullist = list(sumajdata.iloc[:, 1].isnull())
                                    for isumr in range(len(boolnullist)):
                                        if boolnullist[isumr]:
                                            sumajdata.iloc[isumr, 1] = sumajdata.iloc[isumr, 3]
                                            sumajdata.iloc[isumr, 2] = sumajdata.iloc[isumr, 4]
                                    del sumajdata["Temp"]
                                    del sumajdata["Rel. Hum."]
                            else:
                                sumajdata = sumajdata.rename(columns={"Temp": 'T_' + str(iHeight), "Rel. Hum.": 'H_' + str(iHeight)})
                # 作成したsumajdataをシェルフファイルに保存
                shelf_file = shelve.open('./tmp/tempdata')
                while colname in list(shelf_file.keys()):
                    colname = colname + '_2'
                shelf_file[colname] = sumajdata
                shelf_file.close()
            else:
                raise Exception('siteperiod_csvのTypeに不正な形式があります。' + str(iSite) + '行目')
        except Exception as err:
            print('ERROR: ' + str(err))
        if iSite == siteperiod_num - 1:
            tadoutput(iSiteID, tmp_pass, './tmp/tempdata')
        elif iSiteID != siteperiod_csv["SiteID"][iSite + 1]:
            tadoutput(iSiteID, tmp_pass, './tmp/tempdata')
        print("temp_timeadj: " + str(iSite + 1) +  "/"  + str(siteperiod_num) + "列まで終了")
    shutil.rmtree(tmp_pass)

def tadoutput(p_iSiteID, p_tmp_pass, p_shelf_pass):
    shelf_file = shelve.open(p_shelf_pass)
    shelfkeys_list = list(shelf_file.keys())
    len_shelf = len(shelfkeys_list)
    for shnum in range(len_shelf):
        if shnum == 0:
            output = shelf_file[shelfkeys_list[shnum]]
        else:
            output = pd.merge(output, shelf_file[shelfkeys_list[shnum]], on='Time', how='outer')
    shelf_file.close()
    output.sort_values('Time', inplace=True)
    # csvファイル出力する　@ .\timeadj
    if not os.path.exists(r'.\temp_timeadj'):
        os.makedirs(r'.\temp_timeadj')
    out_filename = 'temp_TiAd_' + p_iSiteID + '.csv'
    output.to_csv('.\\temp_timeadj\\' + out_filename, index = False)
    shutil.rmtree(p_tmp_pass)
    os.makedirs(p_tmp_pass)

def modsec(data):
    ## 何秒間隔かを判定する
    # 何分あるかを取得
    d_min = (data.iat[len(data["Time"])-1,0] - data.iat[0,0]).total_seconds() // 60
    # 行数を取得.
    d_nrow = len(data["Time"])
    # 1分当たりの行数を取得（3行なら60/3で20秒間隔）（切り上げ)
    nsec = math.ceil(d_nrow / d_min)
    fmin = -1
    fsec = 0
    count = 0
    for irow in range(len(data["Time"])):
        if data.iat[irow,0].minute == fmin:
            fsec = int(fsec + 60/nsec)
            if data.iat[irow,0].second == 0:
                data.iat[irow,0]= data.iat[irow,0] + timedelta(seconds = fsec)
                count = count + 1
        else:
            fsec = 0
            fmin = data.iat[irow,0].minute
            count = 1
        assert count <= nsec, str(count) + str(nsec) + str(data.iat[irow,0]) + ':modsec関数内において秒の値が60を超えます'