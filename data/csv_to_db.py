import sqlite3
import pandas as pd
import logging
from datetime import datetime

with open('data/data.db','wb+') as file_obj:
    file_obj.close()
con = sqlite3.connect('data/data.db')

logger = logging.getLogger(__name__)


file_handler = logging.FileHandler(f"logs/CONVERT_{datetime.now().strftime('%Y-%m-%d-%H-%M')}.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s"))

logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

logger.info('Proces started')
logger.error('Proces Error')

def update_investment():
    df_invest = pd.read_csv('data/inve.csv')
    df_invest['date'] = pd.to_datetime(df_invest['date']).dt.date
    df_invest.to_sql('investment',con, if_exists='append', index=False)
    logger.info('Investment data successfully stored in DB!')