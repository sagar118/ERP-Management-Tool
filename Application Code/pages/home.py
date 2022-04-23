import streamlit as st
import time
import numpy as np
import pandas as pd

from sql_connect import cur

def app():
    table_names = ["Categories", "Categories Description", "Post Address Lookup", "Supplier", "Products", "Employees", "Territories", "Employee Territories", "Customers", "Shippers", "Orders", "Order Details"]
    table_names.sort()

    if st.button('Say hello'):
        with st.form("insert_form"):
            st.write("Inside the form")
            slider_val = st.slider("Form slider")
            checkbox_val = st.checkbox("Form checkbox")

            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                st.write("slider", slider_val, "checkbox", checkbox_val)


    table = st.sidebar.selectbox("Select Table:", table_names)
    table_name = "_".join(table.lower().split())
    st.write(table)
    cur.execute(f"SELECT * FROM {table_name}")
    colnames = [desc[0] for desc in cur.description]

    result = cur.fetchall()
    st.dataframe(pd.DataFrame(result, columns=colnames))
