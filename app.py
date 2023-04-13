## TODO
# Basic Distribution EDA_Page
# Numerical EDA_Page
# Categorical EDA_Page
# Correlation_Matrix EDA_Page
# ChatGPT Advisory for ML-Commitment

### Libraries come here
import streamlit as st
import numpy as np
import pandas as pd
import pyarrow

### Functions come here


### Page components come here
#### > Handles
st.sidebar.title("Page Handles")

df = pd.read_csv("./dta/sample_data.csv")
uploaded_file = st.sidebar.file_uploader("Choose a File {.csv, .xls, .parquet*}", type=["csv", "xls", "parquet"])

### Read Uploaded data
if uploaded_file is not None:
    if uploaded_file.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.endswith(".parquet"):
        df = pd.read_parquet(uploaded_file)
    else:
        st.error("Provide an acceptable file extension")

### Basic Analytics
shape = df.shape
null_values = sum(df.isnull().sum())

#### > Exploration Page
st.header("Exploratory Data Analysis")
st.markdown("Simple Data Visualization/Exploration Tool for quickly Probing, Visualizing and Analyzing Data Sets")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.text("PlaceHolder: Plot 1")

with col2:
    st.text("PlaceHolder: Plot 2")

st.divider()

st.subheader("Data Page")
st.warning("Check the **Editable Dataframes** option on the side widget to enable you change your values")

### Option to edit data
Editable_Status = {0: "No", 1: "Yes"}
if st.sidebar.checkbox("Would you like to edit your data"):
    st.experimental_data_editor(df, use_container_width=True)
    Editable_Status = Editable_Status[1]
else:
    st.dataframe(df, use_container_width=True)
    Editable_Status = Editable_Status[0]

st.sidebar.divider()

s_Col1, s_Col2, s_Col3 = st.sidebar.columns(3)
with s_Col1:
    st.markdown("### DATA SHAPE")
    st.write(shape)

with s_Col2:
    st.markdown("### EDITABLE STATUS")
    st.write(Editable_Status)

with s_Col3:
    st.markdown("### NULL VALUES")
    st.write(null_values)