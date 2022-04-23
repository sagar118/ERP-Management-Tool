import streamlit as st

# Custom imports 
from multipage import MultiPage
from pages import home#, advanced#, metadata, data_visualize, redundant, inference # import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("ERP System")

# Add all your applications (pages) here
app.add_page("Home", home.app)
# app.add_page('Filter Tables', advanced.app)
# app.add_page("Home 2", blank.app)


# The main app
app.run()