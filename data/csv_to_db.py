import sqlite3
import pandas as pd

with open('data/data.db','wb+') as file_obj:
    file_obj.close()

con = sqlite3.connect('data/data.db')

df_invest = pd.read_csv('data/inve.csv')
df_invest['date'] = pd.to_datetime(df_invest['date']).dt.date

print(df_invest.info())
print(df_invest)

df_invest.to_sql('investment',con, if_exists='append', index=False)
print('Investment data successfully stored in DB!')