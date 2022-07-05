import psycopg2
import pandas as pd
import numpy as np
import glob
import sys
import os

conn = psycopg2.connect(
    host="localhost",
    database="DMQL_Project",
    user="postgres",
    password="PostgreSQL#118")

cur = conn.cursor()


FILE_DIR = "../Data_Files/"

table_insert_order = ["categories", "categories_description", "post_address_lookup", "supplier", "products", "employees", "territories", "employee_territories", "customers", "shippers", "orders", "order_details"]

# for filepath in glob.glob(FILE_DIR + "*.csv"):
for table_name in table_insert_order:
    cur.execute("DELETE FROM "+ table_name)
    conn.commit()

    print(f"Inserting into table: {table_name}")
    data = pd.read_csv(FILE_DIR + table_name + ".csv", encoding='latin1')

    n_cols = data.shape[1]
    col_name = data.columns.values

    # if table_name == "products":
        # data.quantity_per_unit = data.quantity_per_unit.apply(lambda x: int(x.split()[0]))
        # data.discontinued = data.discontinued.apply(lambda x: True if x else False)
    
    # Handle NULL in dataframe
    data.fillna(value=np.nan, inplace=True)
    data = data.replace([np.nan], [None])

    # args_str = ",".join(cur.mogrify("(" + ("%s,"*n_cols).strip(",") + ")", tuple(row)[1:]).decode('utf-8') for row in data.itertuples())   

    col_string = ",".join(col for col in col_name)
    placeholders =  "(" + ("%s,"*n_cols).strip(",") + ")"
    
    cur.executemany("INSERT INTO "+ table_name + " (" + col_string + ") VALUES " + placeholders, data.values.tolist())
    conn.commit()