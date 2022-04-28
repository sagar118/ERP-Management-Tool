import time
import numpy as np
import streamlit as st
import pandas as pd
from sql_connect import cur, conn

def app():
    table_names = ["Customers"]
    table_names.sort()
    table = st.sidebar.selectbox("Select Table:", table_names, on_change= reset_page)
    if(table == 'Customers'):
        table_name = "_".join(table.lower().split())
        call_customers(table_name)
    

def reset_page():
    st.session_state.page_number = 0

def call_customers(table_name):
    cur.execute(f'SELECT DISTINCT ID FROM {table_name}')
    colnames = [desc[0] for desc in cur.description]
    customer_ids = []
    query_result = cur.fetchall()
    for res in query_result:
        customer_ids.append(res[0])
    print(customer_ids)
    customer_id = st.selectbox("Select the customer:", customer_ids)
    

