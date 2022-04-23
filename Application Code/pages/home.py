import time
import numpy as np
import streamlit as st
import pandas as pd
from sql_connect import cur, conn


st.session_state.page_number = 0
st.session_state.submit = False
st.session_state.insert = []
st.session_state.id = 0
st.session_state.name = ''
st.session_state.submit = False

column_dict = {'categories': [['id', 'name'], {'id': 'int64', 'name': 'O'}], 'categories_description': [['category_id', 'description'], {'category_id': 'int64', 'description': 'O'}], 'post_address_lookup': [['city', 'postal_code', 'country'], {'city': 'O', 'postal_code': 'O', 'country': 'O'}], 'supplier': [['id', 'company_name', 'contact_name', 'contact_title', 'postal_code', 'country', 'contact'], {'id': 'int64', 'company_name': 'O', 'contact_name': 'O', 'contact_title': 'O', 'postal_code': 'O', 'country': 'O', 'contact': 'O'}], 'products': [['id', 'name', 'supplier_id', 'category_id', 'quantity_per_unit', 'unit_price', 'stock', 'discontinued'], {'id': 'int64', 'name': 'O', 'supplier_id': 'int64', 'category_id': 'int64', 'quantity_per_unit': 'O', 'unit_price': 'float64', 'stock': 'int64', 'discontinued': 'int64'}], 'employees': [['id', 'last_name', 'first_name', 'title', 'birthdate', 'hire_date', 'postal_code', 'country', 'contact', 'reports_to'], {'id': 'int64', 'last_name': 'O', 'first_name': 'O', 'title': 'O', 'birthdate': 'O', 'hire_date': 'O', 'postal_code': 'O', 'country': 'O', 'contact': 'O', 'reports_to': 'float64'}], 'territories': [['id', 'name'], {'id': 'int64', 'name': 'O'}], 'employee_territories': [['employee_id', 'territory_id'], {'employee_id': 'int64', 'territory_id': 'int64'}], 'customers': [['id', 'name', 'contact_name', 'title', 'postal_code', 'country', 'contact'], {'id': 'O', 'name': 'O', 'contact_name': 'O', 'title': 'O', 'postal_code': 'O', 'country': 'O', 'contact': 'O'}], 'shippers': [['id', 'name', 'contact'], {'id': 'int64', 'name': 'O', 'contact': 'O'}], 'orders': [['id', 'customer_id', 'employee_id', 'order_date', 'delivery_date', 'shipped_date', 'shipper_id', 'weight', 'ship_name', 'ship_postal_code', 'ship_country'], {'id': 'int64', 'customer_id': 'O', 'employee_id': 'int64', 'order_date': 'O', 'delivery_date': 'O', 'shipped_date': 'O', 'shipper_id': 'int64', 'weight': 'float64', 'ship_name': 'O', 'ship_postal_code': 'O', 'ship_country': 'O'}], 'order_details': [['order_id', 'product_id', 'unit_price', 'quantity', 'discount'], {'order_id': 'int64', 'product_id': 'int64', 'unit_price': 'float64', 'quantity': 'int64', 'discount': 'float64'}]}

def insert_table_details(table):
    print('Inside Insert: ', table)
    with st.form("insert_form", clear_on_submit=True):
        st.write("Enter details:")
        
        col_names = column_dict[table][0]
        dtypes = column_dict[table][1]
        values = list()

        for col in col_names:
            print('Inside for loop ',col)
            if dtypes[col] == 'O':
                text = st.text_input(col, key= col)
                # print('Text is: ',text)
                values.append(text)
            if dtypes[col] in ['int64', 'float64']:
                number = st.number_input(col, key= col)
                # print('Number is: ', number)
                values.append(number)
                # st.session_state.insert = values
        print('-'*15)
        # print(values)
        submitted = st.form_submit_button("Submit", on_click=insert_values, args=([table]))
        # print(submitted)
        # if submitted:
        #     print(submitted)
        #     n_cols = len(col_names)
        #     col_string = ",".join(col for col in col_names)
        #     placeholders =  "(" + ("%s,"*n_cols).strip(",") + ")"
        #     # print("INSERT INTO "+ table + " (" + col_string + ") VALUES " + placeholders.format(tuple(values)))
        #     print(st.session_state.insert)
            # cur.execute("INSERT INTO "+ table + " (" + col_string + ") VALUES " + placeholders, tuple(st.session_state.insert))
            # conn.commit
            # st.write("slider", text, "checkbox", number)


def app():
    table_names = ["Categories", "Categories Description", "Post Address Lookup", "Supplier", "Products", "Employees", "Territories", "Employee Territories", "Customers", "Shippers", "Orders", "Order Details"]
    table_names.sort()

    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0
    if 'submit' not in st.session_state:
        st.session_state.submit = False
    table = st.sidebar.selectbox("Select Table:", table_names, on_change= reset_page)
    table_name = "_".join(table.lower().split())

    col_names = column_dict[table_name][0]
    dtypes = column_dict[table_name][1]
    for col in col_names:
        if col not in st.session_state:
            if dtypes[col] == 'O':
                st.session_state[col] = ''
            else:
                st.session_state[col] = 0
    print(table_name)

    # st.button('Insert', on_click = insert_table_details, args=([table_name]))
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        if st.button('Insert'):  
            insert_table_details(table_name)

    with col2:
        if st.button('Delete'):  
            delete_table_details(table_name)
    
    # with col3:
        # if st.button('Update'):  
            # insert_table_details(table_name)

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

        # print('st.session_state.page_number ', st.session_state.page_number)
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
    
def insert_values(table):
    col_names = column_dict[table][0]
    dtypes = column_dict[table][1]
    values = []
    print('Inside the show values')
    for col in col_names:
        values.append(st.session_state[col])
    print("Values: ",values)
    
    n_cols = len(col_names)
    col_string = ",".join(col for col in col_names)
    placeholders =  "(" + ("%s,"*n_cols).strip(",") + ")"
    print("INSERT INTO "+ table + " (" + col_string + ") VALUES " + placeholders.format(tuple(values)))
    # print(st.session_state.insert)
    cur.execute("INSERT INTO "+ table + " (" + col_string + ") VALUES " + placeholders, values)
    conn.commit


def delete_table_details(table):
    print('Inside Delete: ', table)
    with st.form("delete_form", clear_on_submit=True):
        st.write("Enter details:")
        
        col_names = column_dict[table][0]
        dtypes = column_dict[table][1]
        values = list()

        for col in col_names:
            print('Inside for loop ',col)
            if dtypes[col] == 'O':
                text = st.text_input(col, key= col)
                # print('Text is: ',text)
                values.append(text)
            if dtypes[col] in ['int64', 'float64']:
                number = st.number_input(col, key= col)
                # print('Number is: ', number)
                values.append(number)
                # st.session_state.insert = values
        print('-'*15)
        # print(values)
        submitted = st.form_submit_button("Submit", on_click=delete_values, args=([table]))

def delete_values(table):
    col_names = column_dict[table][0]
    dtypes = column_dict[table][1]
    values = []
    print('Inside the show values')
    delete_columns = []
    for col in col_names:
        if dtypes[col] == 'O':
            if st.session_state[col] != '':
                values.append(st.session_state[col])
                delete_columns.append(col)
        
        if dtypes[col] in ['int64', 'float64']:
            if st.session_state[col] != 0:
                values.append(st.session_state[col])
                delete_columns.append(col)
    print("Values: ",values)
    delete_condition = ''
    for i, col in enumerate(delete_columns):
        if type(values[i]) == int or type(values[i]) == float:
            delete_condition += " "+col+" = "+str(values[i])+" and"
        else:
            delete_condition += " "+col+" = '"+str(values[i])+"' and"
    delete_condition = delete_condition.rsplit(' ', 1)[0]
    print("DELETE FROM "+ table + " WHERE "+delete_condition)
    # print(st.session_state.insert)
    cur.execute("DELETE FROM "+ table + " WHERE "+delete_condition)
    conn.commit