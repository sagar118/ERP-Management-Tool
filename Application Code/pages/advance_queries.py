import time
import numpy as np
import streamlit as st
import pandas as pd
from sql_connect import cur, conn

import plotly.figure_factory as ff
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def app():
    use_cases = ["Custom Order Details", "Discontinued Product Orders"]
    use_cases.sort()
    table = st.sidebar.selectbox("Select Use Case", use_cases, on_change= reset_page)
    if(table == 'Custom Order Details'):
        # table_name = "_".join(table.lower().split())
        call_customers("Customers")
    
    elif (table == 'Discontinued Product Orders'):
        call_discrepancies()



def reset_page():
    st.session_state.page_number = 0

def call_customers(table_name):
    cur.execute(f'SELECT DISTINCT ID FROM {table_name}')
    colnames = [desc[0] for desc in cur.description]
    customer_ids = []
    query_result = cur.fetchall()
    for res in query_result:
        customer_ids.append(res[0])
    customer_ids.sort()
    customer_id = st.selectbox("Select the customer:", customer_ids)
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
                o.shipper_id      = s.id
                and o.id          = od.order_id
                and od.product_id = p.id
                and o.customer_id = '{customer_id}'
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
        """.replace('^', '')
    print(query)
    cur.execute(query)
    colnames = [desc[0] for desc in cur.description]
    result = cur.fetchall()
    result = pd.DataFrame(result, columns=colnames)
    st.table(result)