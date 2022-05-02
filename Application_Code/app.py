import streamlit as st
st.set_page_config(layout="wide")
# Custom imports 
from multipage import MultiPage
from pages import home, filter_tables, advance_queries#, metadata, data_visualize, redundant, inference # import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("ERP System")

# Add all your applications (pages) here
app.add_page("Home", home.app)
app.add_page('Filter Tables', filter_tables.app)
app.add_page('Advance Queries', advance_queries.app)
# app.add_page("Home 2", blank.app)


# The main app
app.run()