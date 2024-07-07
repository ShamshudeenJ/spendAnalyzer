import pandas as pd
import altair as alt
import numpy as np
from statistics import geometric_mean

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
    
    def heatmap(self):
        chart = alt.Chart(self.data).mark_rect().encode(
            x = alt.X('year(date):O'),
            y = alt.Y('month(date):O'),
            color = alt.Color('sum(price):Q'),
            tooltip = alt.Tooltip(['yearmonth(date)','sum(price)'])
            ).interactive()
        return chart
    
    def monthly_projection(self):
        chart = alt.Chart(self.data).mark_line().encode(
            x = alt.X('yearmonth(date):T'),
            y = alt.Y('sum(price):Q')
            ).interactive()
        return chart
    
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