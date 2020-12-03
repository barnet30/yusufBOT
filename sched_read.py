import xlrd
import pandas as pd
xl = xlrd.open_workbook("sched.xlsx") # читаете книгу Excel
sheet = xl.sheet_by_index(0) # читаете нужный лист
df =  pd.read_excel("sched.xlsx", header=None)#создаем datframe


print('-------------------------------')
#ищем и заполняем данные в объединенных ячейках
for crange in sheet.merged_cells:
    rl,rh,cl,ch = crange
    merged_value = sheet.cell_value(rl, cl)
    df.iloc[rl:rh,cl:ch] = merged_value
# print(df.iloc[5:21,3])

