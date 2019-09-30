iend = pd.to_datetime("2019/4/30 09:29:30", format=r'%Y/%m/%d %H:%M:%S')
timelist2 = [iend - timedelta(seconds=x) for x in range(0, 7923*30, 30)]
with open('WEATHER - 2134337_2019-04-30 06_52_30', mode = 'w') as f:
    f.writelines(str(timelist2))