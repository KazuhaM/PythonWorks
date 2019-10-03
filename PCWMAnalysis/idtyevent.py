import os

folder_pass = r"E:\Clouds\OneDrive - g.ecc.u-tokyo.ac.jp\LEP\2019\現行資料\0802春季モンゴル解析2\OriginalData"
event_csv = 'EventPeriodinSite.csv'
os.chdir(folder_pass)
event_csv = os.path.join(folder_pass, event_csv)

keventf_csv = pd.read_csv(event_csv, sep=',')