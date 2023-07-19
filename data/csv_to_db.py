import pandas as pd
import sqlite3

con = sqlite3.connect('data/data.db')
df_invest = pd.read_csv('data/inve.csv')
df_invest['date'] = pd.to_datetime(df_invest['date']).dt.date
print(df_invest.info())
print(df_invest)
# df_invest.to_sql('investment',con, if_exists='append', index=False)