import openpyxl
wb = openpyxl.load_workbook('WEATHER - 2122789_2019-05-04 06_30_40.xlsx')
sheet = wb[wb.sheetnames[0]]
ts_value = sheet['A2'].value
type(ts_value)