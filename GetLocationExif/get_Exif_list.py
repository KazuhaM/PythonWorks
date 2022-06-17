from msilib.schema import CompLocator
from PIL import Image
import PIL.ExifTags as ExifTags
import glob
import argparse
import sys
import pandas as pd

# あるフォルダ内の指定の拡張子のファイルリストを取得（フォルダパスもセット）
def get_file_list(foldername, ext=".jpg"):
    photofiles = glob.glob(foldername + '/*' + ext)
    return photofiles

# exifのGPSデータを分数から度に変換
def conv_deg(v):
        d = float(v[0])
        m = float(v[1])
        s = float(v[2])
        return d + (m / 60.0) + (s / 3600.0)

def get_gps(fname):
    # 画像ファイルを開く --- (*1)
    im = Image.open(fname)
    # EXIF情報を辞書型で得る
    exif = {
        ExifTags.TAGS[k]: v
        for k, v in im._getexif().items()
        if k in ExifTags.TAGS
    }
    # GPS情報を得る --- (*2)
    gps_tags = exif["GPSInfo"]
    gps = {
        ExifTags.GPSTAGS.get(t, t): gps_tags[t]
        for t in gps_tags
    }
    # # 緯度経度情報を得る --- (*3)
    lat = conv_deg(gps["GPSLatitude"])
    lat_ref = gps["GPSLatitudeRef"]
    if lat_ref != "N": lat = 0 - lat
    lon = conv_deg(gps["GPSLongitude"])
    lon_ref = gps["GPSLongitudeRef"]
    if lon_ref != "E": lon = 0 - lon
    return lat, lon


if __name__ == "__main__":
    # 引数の処理
    parser = argparse.ArgumentParser(description='フォルダを指定して画像ファイルのexifから座標を取得する')

    parser.add_argument('folderpath', help='画像フォルダが格納されているフォルダのパス')
    parser.add_argument('-e','--ext', help='対象とする画像の拡張子', default='.jpg')

    args = parser.parse_args()

    # フォルダパスの形式指定に関する例外処理
    if args.folderpath[-1] == '/':
        print('フォルダパスの最後は/で終わらないでください')
        sys.exit(0)

    # 緯度経度情報の結果格納データフレーム
    cols = ['filename','lat', 'lon']
    results = pd.DataFrame(columns=cols)

    files = get_file_list(args.folderpath, args.ext)
    files = [s.replace('\\','/') for s in files]

    for i_file in files:
        lat, lon = get_gps(i_file)
        results.loc[len(results)] = {cols[0]: i_file, cols[1]: lat, cols[2]: lon}
    # print(results)
    results.to_csv(args.folderpath + '/' + 'PhotoLocationList.csv')