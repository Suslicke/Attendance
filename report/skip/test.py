from time import strftime
import pandas as pd
import xlwt

wb = xlwt.Workbook(encoding='utf-8')
ws = wb.add_sheet('Октябрь')
period = pd.period_range(start='2022.09.01', end='2023.07.01', freq='D')
columns = []
for x in period:
    columns.append(str(x))
    columns.append("%")

print(columns)