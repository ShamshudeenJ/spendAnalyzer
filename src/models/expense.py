import pandas as pd
import altair as alt

class Expense():
    def __init__(self, file_name):
        self.data = pd.read_csv(file_name)
        self.data['date'] = pd.to_datetime(self.data['date'])
        self.data['price'] = pd.to_numeric(self.data['price'])
    
    def heatmap(self):
        chart = alt.Chart(self.data).mark_rect().encode(
            x = alt.X('year(date):O'),
            y = alt.Y('month(date):O'),
            color = alt.Color('sum(price):Q'),
            tooltip = alt.Tooltip(['yearmonth(date)','sum(price)'])
            ).interactive()
        return chart
    
    def distribution(self):
        self.data_monthly = self.data.groupby(by=[self.data['date'].dt.year, self.data['date'].dt.month])['price'].sum()
        print(self.data_monthly)
        # chart = alt.Chart(self.data_monthly).mark_bar().encode(
        #     x = alt.X('sum(price):Q', bin=True),
        #     y = alt.Y('count()')
        #     ).interactive()
        # return chart