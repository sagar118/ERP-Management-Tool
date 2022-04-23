import streamlit as st
import time
import numpy as np
from sql_connect import cur
import pandas as pd
def app():
    table_names = ["Categories", "Categories Description", "Post Address Lookup", "Supplier", "Products", "Employees", "Territories", "Employee Territories", "Customers", "Shippers", "Orders", "Order Details"]
    table_names.sort()
    table = st.sidebar.selectbox("Select Table:", table_names)
    table_name = "_".join(table.lower().split())
    # st.write(table)
    
    query = f"SELECT * FROM {table_name}"
    
    cur.execute(query)

    colnames = [desc[0] for desc in cur.description]

    result = cur.fetchall()
    data = pd.DataFrame(result, columns=colnames)
    st.dataframe(data)

    cols_to_filter = st.sidebar.multiselect("Select Columns to Filter on", colnames)
    filters = {}
    and_or_string = []
    # if 
    #     filters[cols_to_filter[0]] = st.sidebar.text_input('Enter your filter for {}'.format(cols_to_filter[0]))
    # elif len(cols_to_filter) > 1:
    
    for column in cols_to_filter:
        filters[column] = st.sidebar.text_input('Enter your filter for {} (eg: "< 10 or > 1 or = 5")'.format(column))
        and_or_string.append(st.sidebar.text_input('AND OR after {} condition (leave blank if no other condition)'.format(column)))


    
    print('filters ', filters)
    print('and_or_string ', and_or_string)
    # st.button('Get Result', on_click=get_result(filters, table_name))

def get_result(filters, table_name):
    # query_builder = 
    # st.dataframe(data)
    pass