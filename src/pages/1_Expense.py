import os
import streamlit as st
from models.expense import Expense


st.set_page_config(page_title="Expense", layout="wide")
st.title('Expense Analysis')

exp = Expense(os.path.dirname(__file__)+'/../../data/expense.csv')

with st.expander('Monthly expense', expanded=True):
    st.altair_chart(exp.heatmap(),use_container_width=True)
    st.altair_chart(exp.monthly_projection(), use_container_width=True)

with st.expander('Monthly distribution', expanded=True):
    lt,rt = st.columns([2,1])
    lt.altair_chart(exp.distribution(),use_container_width=True)
    rt.write(f"Mean: Rs.{exp.monthly_stats['mean']}")
    rt.write(f"Geometric Mean: Rs.{exp.monthly_stats['geo_mean']}")
    rt.write(f"Median of **Rs.{exp.monthly_stats['median']} $±$ Rs.{exp.monthly_stats['sd']}**")
    print(exp.monthly_stats['weighted_mean'])
