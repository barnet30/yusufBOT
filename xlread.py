""" Считывание данных из таблицы Excel с объединенными ячейками
Можно использовать .merged_cells из xlrd
см. документацию https://xlrd.readthedocs.io/en/latest/api.html#xlrd.sheet.Sheet.merged_cells
"""
import xlrd
import pandas as pd
xl = xlrd.open_workbook("mergeddata.xlsx") # читаете книгу Excel 
sheet = xl.sheet_by_index(0) # читаете нужный лист 
df =  pd.read_excel("mergeddata.xlsx", header=None)#создаем datframe
print('До преобразования')
print(df)
print(sheet.merged_cells)
#ищем и заполняем данные в объединенных ячейках
for crange in sheet.merged_cells:
    rl,rh,cl,ch = crange
    merged_value = sheet.cell_value(rl, cl)
    df.iloc[rl:rh,cl:ch] = merged_value

print('После преобразования')
print(df)

