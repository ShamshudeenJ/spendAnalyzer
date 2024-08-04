import os
import streamlit as st
from models.expense import Expense


st.set_page_config(page_title="Expense", layout="wide")
st.title('Expense Analysis')

exp = Expense(os.path.dirname(__file__)+'/../../data/expense.csv')

with st.expander('Monthly expense', expanded=True):
    st.table(exp.spent_category())
    # st.altair_chart(exp.spent_category(),use_container_width=True)


