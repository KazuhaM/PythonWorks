#! python3
# timeadj.py -　サイトごとの時刻合わせデータ作成

# package import
import pandas as pd

def initmodPC(p_pcdata_pass):
    ## .\\avebynフォルダ内のファイルについて逐次実行
    # ファイル一覧取得
    originPC_csvpass = os.path.join(p_pcdata_pass, '*.csv')
    originPC_flist = glob.glob(originPC_csvpass)
    # 各ファイルについて実行
    for iitimodPC in originPC_flist
        # ファイル取得
        idataPC_csv = pd.read_csv(iitimodPC, sep=',')
        # 機種コメントを残して、上部情報行を削除
        # "積算"行を2列目で探査して、それ以上の行を削除する