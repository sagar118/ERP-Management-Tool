import streamlit as st

# Custom imports 
from multipage import MultiPage
from pages import firstbase, blank#, metadata, data_visualize, redundant, inference # import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("DMQL Project")

# Add all your applications (pages) here
app.add_page("Upload Data", firstbase.app)
app.add_page("Blank", blank.app)
# app.add_page("Change Metadata", metadata.app)
# app.add_page("Machine Learning", machine_learning.app)
# app.add_page("Data Analysis",data_visualize.app)
# app.add_page("Y-Parameter Optimization",redundant.app)

# The main app
app.run()