import streamlit as st
import time
import numpy as np
import pandas as pd
# from Application_Code.ERP_System.sql_connect import cur, conn
from sql_connect import cur, conn

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

    cols_to_print = st.sidebar.multiselect("Select Columns to Print (Nothing for all columns)", data.columns)

    cols_to_filter = st.sidebar.multiselect("Select Columns to Filter on", colnames)
    filters = {}
    conditions = []
    condition_values = []

    for column in cols_to_filter:
        conditions.append(st.sidebar.selectbox("Enter the condition for {}".format(column), ['=', '<', '>', '<=', '>=', "<>","like", "in", "between", "not like", "not in", "not between", "is null", "is not null", "is true", "is not true", "is false", "is not false"]))
        filters[column] = st.sidebar.text_input('Enter your filter for {} (eg: "10")'.format(column))
        condition_values.append(st.sidebar.selectbox('AND OR after {} condition (Note: Leave Blank if No Other Condition)'.format(column), ['Blank','AND', 'OR']))
    
    form = st.form(key='my-form')
    submit = form.form_submit_button('Get Result')
    if submit:
        get_result(filters, table_name, conditions, condition_values, cols_to_print)

    # st.button('Get Result', on_click=get_result, args = (filters, table_name, and_or_string, cols_to_print))
    # st.button('Get Result', on_click=get_result(filters, table_name, and_or_string, cols_to_print))

def get_result(filters, table_name, conditions, condition_values, cols_to_print):
    query = ""
    if len(cols_to_print) == 0:
        st.write('No specific columns selected for display')
        query += "SELECT * FROM {}".format(table_name)
    else:
        query += "SELECT {} FROM {}".format(', '.join(cols_to_print), table_name)

    
    # st.write('filters ',filters, 'table_name ', table_name, "conditions ",conditions, "condition_values ", condition_values, "cols_to_print ",cols_to_print)
    if bool(filters):
        keys, values = zip(*filters.items())
        query += " WHERE "
        for key, value, condition, joining_value in zip(keys, values, conditions, condition_values):
            if str(value).isdigit():
                query +="{} {} {} ".format(key, condition, value)
            else:
                query +="{} {} '{}' ".format(key, condition, value)
            if joining_value != 'Blank':
                query += " {} ".format(joining_value)
    # st.write(query)
    try:
        cur.execute(query)
        colnames = [desc[0] for desc in cur.description]
        result = cur.fetchall()
        data = pd.DataFrame(result, columns=colnames)
        st.dataframe(data)
        # print('filters ',filters, 'table_name ', table_name, "conditions ",conditions, "condition_values ", condition_values, "cols_to_print ",cols_to_print)
    except Exception as e:
        print("Bad Query: ", e)
