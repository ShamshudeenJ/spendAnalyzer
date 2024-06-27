import os
import streamlit as st
from models.expense import Expense


st.set_page_config(page_title="Expense", layout="wide")
st.title('Expense Analysis')

exp = Expense(os.path.dirname(__file__)+'/../../data/expense.csv')

with st.expander('Monthly expense', expanded=True):
    st.altair_chart(exp.heatmap(),use_container_width=True)

with st.expander('Monthly distribution', expanded=True):
    st.altair_chart(exp.distribution(),use_container_width=True)