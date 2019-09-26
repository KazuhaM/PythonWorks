import csv
import datetime
exfile = open('WEATHER - 2122789_2019-05-04 06_30_40.csv')
exreader = csv.reader(exfile)
exdata = list(exreader)
#exdate = datetime.datetime(exdata[1][0])
exdate = datetime.datetime.strptime(exdata[1][0], "%Y-%m-%d %H:%M:%S")
exdate.second