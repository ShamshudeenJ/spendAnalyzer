import pandas as pd
import altair as alt
import numpy as np
from statistics import geometric_mean
from prophet import Prophet
import json
import os


class Expense():
    def __init__(self, file_name):
        self.data = pd.read_csv(file_name)
        self.data['date'] = pd.to_datetime(self.data['date'])
        self.data['price'] = pd.to_numeric(self.data['price'])
        self.monthly_stats = {}
        self.config = {}
        self.data_monthly = self.data.groupby(by=[self.data['date'].dt.year.rename('year'),
                                                  self.data['date'].dt.month.rename('month')])['price'].sum()
        self.data_monthly = self.data_monthly.reset_index()
        self.data_monthly['date'] = self.data_monthly['year'].astype(str) + '-' + self.data_monthly['month'].astype(str)
        self.data_monthly.index = pd.to_datetime(self.data_monthly['date'])
        self.data_monthly = self.data_monthly.resample('M').last()
        self.data_monthly.index.name = None
    
    def create_config(self):
        df = self.datadf = self.data
        items = df['item'].unique()
        item_map = {k:'' for k in items}

        # Remove spaces
        for k in item_map:
            item_map[k] = {}
            item_map[k]['label'] = k.replace(" ","")
    
        # Split camelCase in to two words
        for k in item_map:
            if item_map[k]['label'][0].islower():
                res = [idx for idx in range(len(item_map[k]['label'])) if item_map[k]['label'][idx].isupper()]
                res.insert(0,0)
                if res:
                    parts = [item_map[k]['label'][i:j] for i,j in zip(res, res[1:]+[None])]
                    item_map[k]['label'] = parts
                else:
                    item_map[k]['label'] = item_map[k]['label']
        with open('src/models/item_map.json','w') as fo:
            json.dump(item_map, fo, indent=4)


    def spent_category(self):
        df = self.data
        self.create_config()
        
        return df['item'].value_counts()

    def heatmap(self):
        chart = alt.Chart(self.data).mark_rect().encode(
            x = alt.X('year(date):O'),
            y = alt.Y('month(date):O'),
            color = alt.Color('sum(price):Q'),
            tooltip = alt.Tooltip(['yearmonth(date)','sum(price)'])
            ).interactive()
        return chart
    
    def monthly_projection(self):
        # chart = alt.Chart(self.data).mark_line().encode(
        #     x = alt.X('yearmonth(date):T'),
        #     y = alt.Y('sum(price):Q')
        #     ).interactive()
        df_proj = pd.DataFrame(self.data_monthly['price'])
        df_proj = df_proj.reset_index()
        df_proj = df_proj.rename(columns={'index':'ds','price':'y'})

        p_model = Prophet()
        p_model.fit(df_proj)
        future = p_model.make_future_dataframe(periods=5, freq='ME')
        forecast = p_model.predict(future)
        forecast = forecast.round()

        trend = alt.Chart(forecast).mark_line(color='green').encode(
            x = alt.X('ds:T', axis=alt.Axis(format="%b-%Y")),
            y = alt.Y('trend:Q'))
        yhat = alt.Chart(forecast).mark_circle().encode(
            x = alt.X('ds:T'),
            y = alt.Y('yhat:Q'))
        yhat_lower = alt.Chart(forecast).mark_circle(color='red').encode(
            x = alt.X('ds:T'),
            y = alt.Y('yhat_lower:Q'))
        chart = alt.layer(trend, yhat, yhat_lower)
        yhat_upper = alt.Chart(forecast).mark_circle(color='red').encode(
            x = alt.X('ds:T'),
            y = alt.Y('yhat_upper:Q'))
        chart = alt.layer(trend, yhat)#,yhat_lower, yhat_upper)
        return chart.interactive()
    
    def distribution(self):
        chart = alt.Chart(self.data_monthly).mark_bar().encode(
            x = alt.X('price:Q', bin=True),
            y = alt.Y('count()'),
            color = alt.value('green')
            ).properties(width=600).interactive()
        self.monthly_stats['mean'] = round(self.data_monthly['price'].mean())
        self.monthly_stats['median'] = round(self.data_monthly['price'].median())
        self.monthly_stats['sd'] = round(self.data_monthly['price'].std())
        self.monthly_stats['geo_mean'] = round(geometric_mean(self.data_monthly['price']))
        self.data_monthly['weights'] = 1* (1 - 0.05)**np.arange(len(self.data_monthly['price']))[::-1]

        self.data_monthly['weighted_price'] = (self.data_monthly['price'] * self.data_monthly['weights'])

        self.monthly_stats['weighted_mean'] = self.data_monthly['weighted_price'].mean()
        return chart