import streamlit as st
import time
import numpy as np
import pandas as pd
from sql_connect import cur

st.session_state.page_number = 0
def app():
    table_names = ["Categories", "Categories Description", "Post Address Lookup", "Supplier", "Products", "Employees", "Territories", "Employee Territories", "Customers", "Shippers", "Orders", "Order Details"]
    table_names.sort()

    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0
    table = st.sidebar.selectbox("Select Table:", table_names, on_change= reset_page)
    table_name = "_".join(table.lower().split())
    st.write(table)
    cur.execute(f"SELECT * FROM {table_name}")
    colnames = [desc[0] for desc in cur.description]

    result = cur.fetchall()
    # st.table(pd.DataFrame(result))
    result = pd.DataFrame(result, columns=colnames)
    
    n = 20
    last_page = len(result) // n
    if(len(result) > 20):
        prev, _ ,next = st.columns([1, 10, 1])
        # print(prev, next)
        
        if next.button("Next"):

            if st.session_state.page_number + 1 > last_page:
                st.session_state.page_number = 0
            else:
                st.session_state.page_number += 1

        if prev.button("Previous"):

            if st.session_state.page_number - 1 < 0:
                st.session_state.page_number = last_page
            else:
                st.session_state.page_number -= 1

        print('st.session_state.page_number ', st.session_state.page_number)
        # Get start and end indices of the next page of the dataframe
        start_idx = st.session_state.page_number * n 
        end_idx = (1 + st.session_state.page_number) * n
        x = st.session_state.page_number
    # print("Session State: ", start_idx, end_idx, st.write(st.session_state.page_number))
    # Index into the sub dataframe
        sub_df = result.iloc[start_idx:end_idx]
        st.table(sub_df)
    else:
        st.table(result)
def reset_page():
        st.session_state.page_number = 0     
    
