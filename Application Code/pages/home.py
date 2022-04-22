import streamlit as st
import time
import numpy as np
import pandas as pd

from sql_connect import cur

def app():
    table_names = ["Categories", "Categories Description", "Post Address Lookup", "Supplier", "Products", "Employees", "Territories", "Employee Territories", "Customers", "Shippers", "Orders", "Order Details"]
    table_names.sort()

    table = st.sidebar.selectbox("Select Table:", table_names)
    table = "_".join(table.lower().split())
    st.write(table)
    cur.execute(f"SELECT * FROM {table}")
    result = cur.fetchall()
    st.write(pd.DataFrame(result))
