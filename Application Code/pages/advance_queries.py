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
    use_cases = ["Custom Order Details", "Discontinued Product Orders", "Delivery Lag Analysis"]
    # use_cases.sort()
    table = st.sidebar.selectbox("Select Use Case", use_cases, on_change= reset_page)
    if (table == 'Custom Order Details'):
        # table_name = "_".join(table.lower().split())
        call_customers("Customers")
    
    elif (table == 'Discontinued Product Orders'):
        call_discrepancies()
    
    elif (table == 'Delivery Lag Analysis'):
        call_delivery_lag()



def reset_page():
    st.session_state.page_number = 0

def call_customers(table_name):
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
        and products.name = '{product_name}'
    order by
        orders.id
        """.replace('^', '')
    
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
    