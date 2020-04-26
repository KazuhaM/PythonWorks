#! python3
# avebyn.py -　サイトごとの時刻合わせデータ作成

#     ## 関数実行
#     # 引数：ファイルの名前（excep_flist）, avetime(何秒間で平均を取るか), timesep
#     # 出力データ： (csvファイル in .\\avebyn)
#     avebyn.avebyn(iexcep, avetime, timesep)

# package import
import pandas as pd
import os
from datetime import timedelta
import numexpr
import statistics
import numpy as np
import re

# 引数：ファイルの名前（excep_flist）, avetime(何秒間で平均を取るか), timesep
# 出力データ： (csvファイル in .\\avebyn)
def avebyn(p_iexcep, p_avetime, p_timesep):
    dataf_csv = pd.read_csv(p_iexcep, sep=',')
    dataf_csv["Time"] = pd.to_datetime(dataf_csv["Time"], format=r'%Y-%m-%d %H:%M:%S')
    wm_firstcol = dataf_csv.columns.get_loc(str([s for s in list(dataf_csv.columns) if re.match(r'T_.+', s)][0]))-1
    group_nrow = int(p_avetime / p_timesep)

    # 各列の間隔を算出して、各列について適切な値の個数をリストで取得
    real_nrow_group = sepmode(dataf_csv)
    ntimelist = np.array([group_nrow]*len(real_nrow_group['mode']))
    real_nrow_group_np = np.array(real_nrow_group['mode'])
    truenrow_eachcol = (ntimelist / real_nrow_group_np).tolist()
    truenrow_eachcol = list(map(toint, truenrow_eachcol))
    truenrow_eachcol = [group_nrow] + truenrow_eachcol

    # 平均結果入力用
    result_dataf = dataf_csv.iloc[0:0]

    for inowr in range(len(dataf_csv)-p_avetime):
        idata_totalsec = dataf_csv.iat[inowr,0].minute * 60 + dataf_csv.iat[inowr,0].second
        nextr = inowr + group_nrow
        if idata_totalsec % p_avetime == 0 and \
             dataf_csv.iat[inowr,0] + timedelta(seconds=p_avetime) == dataf_csv.iat[nextr,0]:
            # 平均を算出するグループで区切ったデータフレームを作成
            temp_group = dataf_csv.iloc[inowr : nextr,:]
            nonan_group = list(temp_group.count())

            if nonan_group == truenrow_eachcol:
                ave_list = np.array(temp_group.sum())
                nonan_group = np.array(nonan_group[1:])
                ave_list[0:wm_firstcol] = ave_list[0:wm_firstcol] / p_avetime
                ave_list[wm_firstcol:] = ave_list[wm_firstcol:] / nonan_group[wm_firstcol:]
                ave_series = pd.Series([dataf_csv.iat[inowr,0]] + ave_list.tolist(), \
                    index = result_dataf.columns, name = len(result_dataf) )
                result_dataf = result_dataf.append(ave_series)
            # データフレームの各列でNULLでない値の個数を数える
            # 値の個数について、実際と、最大値でありかつ適正値である個数とが等しいか判定
            # 等しければ、各列で平均値を算出し（合計値を適正個数で除算）、リストave_listに入れる
            # リストave_listをseriesデータ型に変更し(ave_series)、result_datafに新たな行として追加する
            # 時刻の値は開始時刻にする

    if not os.path.exists('.\\temp_avebyn'):
       os.makedirs('.\\temp_avebyn')
    out_filename = 'temp_Av' + str(p_avetime) + '_' + (os.path.basename(p_iexcep)).replace('temp_Ex_', '')
    result_dataf.to_csv('.\\temp_avebyn\\' + out_filename, index = False)
    print("avebyn: " + out_filename + "まで終了")
## 要件
# 分の下桁が0 or 5 になる時刻から開始して、avetimeを加算したときに最大になる時刻までの平均
# （ex. 300秒なら 2019/5/1/ 15:25:00 ～　2019/5/1/ 15:29:50）
# 時刻の値は開始時刻にする
# 平均を取る際、その時刻内のすべての列の値の個数が最大値になっているか確認（欠損値がないかどうか）
# 欠損値があるかどうかは以下の判定に帰する
# 間隔の最頻値にtimesepをかけた値をその列の間隔の秒とし、avetimeを間隔の秒で除算した値が個数の最大値になる
# 欠損値がある場合は出力しない（出力結果には欠損値が入らないようにする）

# 各列の間隔の最頻値をリスト形式でとってくる関数
# tempデータフレームに代入
# 各列について、NULLでない行のindexを数値形式でとってくる
# 一つ前のindexとの差分を取り、集計する（最頻値、最小値、数量を出す）
# 列ごとに実行し、リスト形式で出力する
def sepmode(p_data):
    ncol = len(p_data.columns)
    sep_result = {'mode':[], 'min':[], 'nrow_notnan':[]}
    for icol in range(1,ncol):
        # 各列について
        icol_data = p_data.iloc[:,icol]
        # 欠損値でない行の探査
        notnan_index_bool = icol_data.isnull()
        notnan_index_bool = [not i for i in notnan_index_bool]
        # 欠損値でない、値が入った行の行番号リストを取得
        notnan_index = icol_data.index[notnan_index_bool]
        dis_index = []
        # 値が入った行に対して、次に値が入る行までいくつ行があるか（次の行なら1）を各値がある行について計算
        # これが、値がある行の間隔に関するリストになる
        for i in range(len(notnan_index)-1):
            dis_index = dis_index + [notnan_index[i +1 ]- notnan_index[i]]
        # 値のある間隔についての最頻値、最小値、及び値のある行の数を出す
        sep_result['mode'] = sep_result['mode'] + [statistics.mode(dis_index)]
        sep_result['min'] = sep_result['min'] + [min(dis_index)]
        sep_result['nrow_notnan'] = sep_result['nrow_notnan'] + [len(notnan_index)]
    return sep_result

def toint(n):
    return int(n)