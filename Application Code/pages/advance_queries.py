import time
import numpy as np
import streamlit as st
import pandas as pd
from sql_connect import cur, conn
import datetime

import plotly.figure_factory as ff
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def app():
    use_cases = ["Custom Order Details", "Employee Order Details", "Discontinued Product Orders", "Delivery Lag Analysis","Popular Categories", "Employee Hierarchy"]
    # use_cases.sort()
    table = st.sidebar.selectbox("Select Use Case", use_cases, on_change= reset_page)
    if (table == 'Customer Order Details'):
        # table_name = "_".join(table.lower().split())
        call_customers("Customers")
    
    elif (table == 'Discontinued Product Orders'):
        call_discrepancies()
    
    elif (table == 'Delivery Lag Analysis'):
        call_delivery_lag()

    elif (table == 'Employee Order Details'):
        call_employee_order_details()
    elif (table == 'Popular Categories'):
        call_popular_categories()

    elif (table == "Employee Hierarchy"):
        call_employee_hierarchy()



def reset_page():
    st.session_state.page_number = 0

def call_customers(table_name):

    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0

    cur.execute(f'SELECT ID, NAME FROM {table_name}')
    colnames = [desc[0] for desc in cur.description]
    customers = []
    query_result = cur.fetchall()
    for res in query_result:
        customers.append(res[0]+' - '+res[1])
    customers.sort()
    customer = st.selectbox("Select the customer:", customers)
    customer_id = customer.split('-')[0].strip()
    where_conditions = "o.shipper_id = s.id and o.id = od.order_id and od.product_id = p.id and o.customer_id = '"+ customer_id+"'"
    cur.execute(f"""Select 
        o.id as order_id
       , o.order_date
       , o.shipped_date
       , o.delivery_date
       , s.name as shippers_name
       , p.name as product_name
       , od.quantity
       , od.unit_price
       , od.discount
       , od.quantity * od.unit_price * (1 - od.discount) as total_price
        from
                orders        o
            , shippers      s
            , order_details od
            , products      p
        where
                {where_conditions}
        order by
                o.id
        ;"""
    )
    colnames_filters = [desc[0] for desc in cur.description]
    result_filters = cur.fetchall()
    result_filters = pd.DataFrame(result_filters, columns=colnames_filters)

    order_ids = list(set(result_filters.loc[:,'order_id']))
    order_ids.sort()
    order_ids.insert(0,'')
    # order_ids
    order_id = st.selectbox("Order Id:", order_ids)
    # print(order_id)
    if order_id:
        where_conditions += " and o.id = "+ str(order_id)

    order_dates = list(set(result_filters.loc[:,'order_date']))
    order_dates = sorted(order_dates)
    order_date = st.date_input("Order Date", [order_dates[0], order_dates[-1]])
    print(order_date, type(order_date))
    where_conditions += " AND o.order_date BETWEEN '"+ str(order_date[0]) +"' and '" + str(order_date[1]) +"'"


    cur.execute(f"""Select 
        o.id as order_id
       , o.order_date
       , o.shipped_date
       , o.delivery_date
       , s.name as shippers_name
       , p.name as product_name
       , od.quantity
       , od.unit_price
       , od.discount
       , od.quantity * od.unit_price * (1 - od.discount) as total_price
        from
                orders        o
            , shippers      s
            , order_details od
            , products      p
        where
                {where_conditions}
        order by
                o.id
        ;"""
    )
    colnames = [desc[0] for desc in cur.description]
    result = cur.fetchall()
    result = pd.DataFrame(result, columns=colnames)

    n = 20
    last_page = len(result) // n
    if(len(result) > 20):
        prev, _ ,next = st.columns([1, 10, 1])
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

        start_idx = st.session_state.page_number * n 
        end_idx = (1 + st.session_state.page_number) * n
    
    if(len(result) > 20):
        sub_df = result.iloc[start_idx:end_idx]
        st.table(sub_df)
    else:
        st.table(result)
    fig = px.bar(result, x="order_date", y="total_price", color="shippers_name")
    st.plotly_chart(fig, use_container_width=True)


def call_employee_order_details():

    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0

    cur.execute(f'SELECT ID, FIRST_NAME, LAST_NAME FROM EMPLOYEES')
    colnames = [desc[0] for desc in cur.description]
    employees = []
    query_result = cur.fetchall()
    for res in query_result:
        employees.append(str(res[0])+' - '+res[1] +' '+res[2])
    employees.sort()
    employee = st.selectbox("Select the Employee:", employees)
    employee_id = employee.split('-')[0].strip()
    where_conditions = "o.shipper_id = s.id and o.id = od.order_id and od.product_id = p.id and o.customer_id = c.id and o.employee_id = "+ str(employee_id)
    cur.execute(f"""Select 
        o.id as order_id
       , c.id as customer_id
       , c.name as customer_name
       , o.order_date
       , o.shipped_date
       , o.delivery_date
       , s.name as shippers_name
       , p.name as product_name
       , od.quantity
       , od.unit_price
       , od.discount
       , od.quantity * od.unit_price * (1 - od.discount) as total_price
        from
                orders        o
            , shippers      s
            , order_details od
            , products      p
            , customers    c
        where
                {where_conditions}
        order by
                o.id
        ;"""
    )
    colnames_filters = [desc[0] for desc in cur.description]
    result_filters = cur.fetchall()
    result_filters = pd.DataFrame(result_filters, columns=colnames_filters)

    order_ids = list(set(result_filters.loc[:,'order_id']))
    order_ids.sort()
    order_ids.insert(0,'')
    # order_ids
    order_id = st.selectbox("Order Id:", order_ids)
    # print(order_id)
    if order_id:
        where_conditions += " and o.id = "+ str(order_id)

    order_dates = list(set(result_filters.loc[:,'order_date']))
    order_dates = sorted(order_dates)
    order_date = st.date_input("Order Date", [order_dates[0], order_dates[-1]])
    print(order_date, type(order_date))
    where_conditions += " AND o.order_date BETWEEN '"+ str(order_date[0]) +"' and '" + str(order_date[1]) +"'"

    customer_dict = {}
    for row in result_filters.itertuples():
        if(row[3] not in customer_dict):
            customer_dict[row[3]] = row[2]

    customer_names = list(sorted(customer_dict.keys()))
    customer_names.insert(0,'')
    customer_name = st.selectbox("Customer:", customer_names)
    # print(order_id)
    if customer_name:
        where_conditions += " and c.id = '"+ str(customer_dict[customer_name]) +"'"

    cur.execute(f"""Select 
        o.id as order_id
       , c.name as customer_name
       , o.order_date
       , o.shipped_date
       , o.delivery_date
       , s.name as shippers_name
       , p.name as product_name
       , od.quantity
       , od.unit_price
       , od.discount
       , od.quantity * od.unit_price * (1 - od.discount) as total_price
        from
                orders        o
            , shippers      s
            , order_details od
            , products      p
            , customers    c
        where
                {where_conditions}
        order by
                o.id
        ;"""
    )
    colnames = [desc[0] for desc in cur.description]
    result = cur.fetchall()
    result = pd.DataFrame(result, columns=colnames)

    n = 20
    last_page = len(result) // n
    if(len(result) > 20):
        prev, _ ,next = st.columns([1, 10, 1])
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

        start_idx = st.session_state.page_number * n 
        end_idx = (1 + st.session_state.page_number) * n
    
    if(len(result) > 20):
        sub_df = result.iloc[start_idx:end_idx]
        st.table(sub_df)
    else:
        st.table(result)
    fig = px.bar(result, x="order_date", y="total_price", color="shippers_name")
    st.plotly_chart(fig, use_container_width=True)


def call_discrepancies():
    query = """
    select
        products.name as product_name,
        count(*) as count
    from
        orders left join order_details on orders.id = order_details.order_id 
        left join products on order_details.product_id = products.id
    where
        products.discontinued = True
    group by
        products.name"""

    cur.execute(query)
    colnames = [desc[0] for desc in cur.description]
    result = cur.fetchall()
    result = pd.DataFrame(result, columns=colnames)
    product_name = st.selectbox("Select the Product for more details:", result['product_name'])
    print("Selected Product: ", product_name)
    st.table(result)
    query = f"""
    select
        orders.id, 
        orders.order_date, 
        orders.shipped_date, 
        orders.delivery_date,
        orders.shipped_date - orders.delivery_date as delay,
        order_details.quantity,
        order_details.unit_price,
        order_details.discount,
        order_details.quantity * order_details.unit_price * (1 - order_details.discount) as total_price,
        products.name as product_name,
        products.discontinued as discontinued
    from
        orders left join order_details on orders.id = order_details.order_id 
        left join products on order_details.product_id = products.id
    where
        products.discontinued = True
        and products.name = '{product_name.replace("'", "''")}'
    order by
        orders.id
        """
    
    print(query)
    cur.execute(query)
    colnames = [desc[0] for desc in cur.description]
    result = cur.fetchall()
    result = pd.DataFrame(result, columns=colnames)
    st.table(result)


def call_delivery_lag():
    options = ["All", "Delayed", "Not Delayed"]
    option = st.selectbox("Select the option:", options)
    if option == "All":
        query = """
        select
            orders.id, 
            orders.order_date, 
            orders.shipped_date, 
            orders.delivery_date,
            orders.shipped_date - orders.delivery_date as delay,
            order_details.quantity,
            order_details.unit_price,
            order_details.discount,
            order_details.quantity * order_details.unit_price * (1 - order_details.discount) as total_price,
            products.name as product_name
        from
            orders left join order_details on orders.id = order_details.order_id 
            left join products on order_details.product_id = products.id
        order by
            total_price desc
        """
        query2 = """
        select
            orders.shipped_date,
            sum(order_details.quantity * order_details.unit_price * (1 - order_details.discount)) as sum_of_price
        from
            orders left join order_details on orders.id = order_details.order_id 
            left join products on order_details.product_id = products.id
        group by 
            orders.shipped_date
        """
    elif option == "Delayed":
        query = """
        select
            orders.id, 
            orders.order_date, 
            orders.shipped_date, 
            orders.delivery_date,
            orders.shipped_date - orders.delivery_date as delay,
            order_details.quantity,
            order_details.unit_price,
            order_details.discount,
            order_details.quantity * order_details.unit_price * (1 - order_details.discount) as total_price,
            products.name as product_name
        from
            orders left join order_details on orders.id = order_details.order_id 
            left join products on order_details.product_id = products.id
        where
            orders.shipped_date - orders.delivery_date > 0
        order by
            total_price desc
        """
        query2 = """
        select
            orders.shipped_date,
            sum(order_details.quantity * order_details.unit_price * (1 - order_details.discount)) as sum_of_price
        from
            orders left join order_details on orders.id = order_details.order_id 
            left join products on order_details.product_id = products.id
        where
            orders.shipped_date - orders.delivery_date > 0
        group by 
            orders.shipped_date
        """
        
    elif option == "Not Delayed":
        query = """
        select
            orders.id, 
            orders.order_date, 
            orders.shipped_date, 
            orders.delivery_date,
            orders.shipped_date - orders.delivery_date as delay,
            order_details.quantity,
            order_details.unit_price,
            order_details.discount,
            order_details.quantity * order_details.unit_price * (1 - order_details.discount) as total_price,
            products.name as product_name
        from
            orders left join order_details on orders.id = order_details.order_id 
            left join products on order_details.product_id = products.id
        where
            orders.shipped_date - orders.delivery_date <= 0
        order by
            total_price desc
        """
        query2 = """
        select
            orders.shipped_date,
            sum(order_details.quantity * order_details.unit_price * (1 - order_details.discount)) as sum_of_price
        from
            orders left join order_details on orders.id = order_details.order_id 
            left join products on order_details.product_id = products.id
        where
            orders.shipped_date - orders.delivery_date <= 0
        group by 
            orders.shipped_date
        """
    cur.execute(query)
    colnames = [desc[0] for desc in cur.description]
    result = cur.fetchall()
    result = pd.DataFrame(result, columns=colnames)
    st.table(result.head(10))

    cur.execute(query2)
    
    colnames = [desc[0] for desc in cur.description]
    result = cur.fetchall()
    result = pd.DataFrame(result, columns=colnames)
    fig = px.bar(result, x="shipped_date", y="sum_of_price")
    st.plotly_chart(fig, use_container_width=True)
    
def call_popular_categories():
    query = """
    select
        categories.name,
        sum(order_details.quantity * order_details.unit_price * (1 - order_details.discount)) as sum_of_price,
        sum(order_details.quantity * order_details.unit_price * (1 - order_details.discount)) / sum(order_details.quantity) as avg_price,
        sum(order_details.quantity) as total_units
    from
        orders left join order_details on orders.id = order_details.order_id 
        left join products on order_details.product_id = products.id
        left join categories on products.category_id = categories.id
    group by 
        categories.name
    order by
        sum_of_price desc
    """
    cur.execute(query)
    colnames = [desc[0] for desc in cur.description]
    result = cur.fetchall()
    result = pd.DataFrame(result, columns=colnames)
    st.table(result)

    fig = px.pie(result, values='sum_of_price', names='name', title='% Sales Per Category')
    # fig.show()
    st.plotly_chart(fig, use_container_width=True)


def call_employee_hierarchy():
    ## Recursive query to get the employee hierarchy
    
    query = """
    With RECURSIVE employee_hierarchy(id, first_name, last_name, manager_id, level) AS (
        SELECT
            id,
            first_name,
            last_name,
            reports_to,
            0
        FROM
            employees
        UNION ALL
        SELECT
            e.id,
            e.first_name,
            e.last_name,
            e.reports_to,
            eh.level + 1
        FROM
            employees e
        JOIN
            employee_hierarchy eh ON e.reports_to = eh.id
    )
    select level, string_agg(distinct(first_name), ',') from employee_hierarchy group by level order by level desc
    """
    cur.execute(query)
    colnames = [desc[0] for desc in cur.description]
    result = cur.fetchall()
    result = pd.DataFrame(result, columns=colnames)

    # This table contains the employee hierarchy, we need to refine the results for the final display.
    for i in range(len(result)-1):
        print(i)
        string1 = result.loc[i,'string_agg']
        for j in range(i+1, len(result)):
            string2 = result.loc[j,'string_agg']
            for sub_string in string2.split(','):
                if sub_string in string1:
                    result.loc[j,'string_agg'] = result.loc[j,'string_agg'].replace(sub_string, '').replace(',,', ',')
                    result.loc[j,'string_agg'] = result.loc[j,'string_agg'].lstrip(',')
                    result.loc[j,'string_agg'] = result.loc[j,'string_agg'].rstrip(',')
    st.table(result)
