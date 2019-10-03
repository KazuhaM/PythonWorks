#! python3
# sepevent.py -　サイトごとの時刻合わせデータ作成

# package import
import pandas as pd
import os

## 関数実行
# 引数：ファイルの名前, event_csv
# 出力データ： (csvファイル in .\\sepevent)
def sepevent(p_event_csv):
    eventf_csv = pd.read_csv(p_event_csv, sep=',')
    eventf_csv["Start"] = pd.to_datetime(eventf_csv["Start"], format=r'%Y-%m-%d %H:%M:%S')
    eventf_csv["End"] = pd.to_datetime(eventf_csv["Start"], format=r'%Y-%m-%d %H:%M:%S')
    nevent = len(eventf_csv)

    avebynf_csvpass = os.path.join(folder_pass, 'avebyn', '*.csv')
    avebynf_flist = glob.glob(avebynf_csvpass)

    # 平均結果入力用
    result_dataf = dataf_csv.iloc[0:0]

    for ievent in range(nevent):
        # 各イベントの最初と最後を取得
        # イベント名を取得
        iEventID = eventf_csv["EventID"][ievent]
        iStart = eventf_csv["Start"][ievent]
        iEnd = eventf_csv["End"][ievent]

        for avebyn_f in avebynf_flist:
            # 平均済みのファイルを開く（avebyn_f）
            tmpave_csv = pd.read_csv(avebynf_flist[avebyn_f], sep=',')
            # そのファイルの最初の日時と最後の日時を取得
            tmpave_csv["Time"] = pd.to_datetime(tmpave_csv["Time"], format=r'%Y/%m/%d %H:%M:%S')
            # 最初と最後の時刻を取る
            fStart = tmpave_csv.iat[0,0]
            fend = tmpave_csv.iat[len(tmpave_csv["Time"])-1,0]
            if not fend <= iStart and not iEnd <= fStart:
                # イベント期間に該当する行を取得
                result_dataf

    if not os.path.exists('.\\sepev'):
       os.makedirs('.\\sepev')
    out_filename = 'Ev_' + os.path.basename(p_event_csv)
    result_dataf.to_csv('.\\sepev\\' + out_filename, index = False)
    print("sepev: " + (os.path.basename(p_event_csv)).replace('.csv', '') + "まで終了")