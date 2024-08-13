### Import Dependencies
import streamlit as st
import pandas as pd
import plotly.express as px
import chardet
import logging

st.set_page_config(page_title="Automated EDA", page_icon="📈")
st.title("Exploratory Data Analysis")

## Initiate Session State


### Placeholder Data
df = pd.read_csv("./dta/sample_data.csv")

# List of common encodings to try
encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']

### Page components come here
#### > Handles
with st.sidebar:
    st.title("Page Handles")
    uploaded_file = st.file_uploader("Choose a File {.csv, .parquet}", type=["csv", "parquet"])

# Read Uploaded data
if uploaded_file is not None:
    # Get the contents of the uploaded file
    file_contents = uploaded_file.getvalue()
    # Store the file contents in the session state
    st.session_state.uploaded_file = file_contents
    if uploaded_file.name.endswith(".csv"):
        for encoding in encodings:
            try:
                logging.info("Ingesting Data")
                df = pd.read_csv(uploaded_file, encoding=encoding, low_memory=False)
                break  # If the file was read successfully, break the loop
            except UnicodeDecodeError as ue:
                logging.info(f"Hit {ue} - Trying next encoding")
        else:  # If none of the encodings worked, raise an error
            raise UnicodeDecodeError("None of the tried encodings worked")
    elif uploaded_file.name.endswith(".parquet"):
        df = pd.read_parquet(uploaded_file)
    else:
        st.error("Provide an acceptable file extension")
        st.stop()
else:
    st.warning("You are currently viewing a MOCK sample")
    # st.stop()


### Data Wrangling
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
numeric_df = df.select_dtypes(include=numerics)
numeric_columns = numeric_df.columns.tolist()
category_df = df.drop(columns=numeric_columns)
category_columns = category_df.columns.tolist()

### Basic Analytics
shape = df.shape
null_values = sum(df.isnull().sum())


#### > Exploration Page
st.header("Exploratory Data Analysis")
st.markdown("Simple Data Visualization/Exploration Tool for quickly Probing, Visualizing and Analyzing Data Sets")

st.divider()
st.markdown('#### Univariate Analysis')
# st.markdown("<h5 style='text-align: center;'>Univariate Analysis</h5>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    num_option = st.selectbox("Select Distribution of a Numerical Variable", numeric_columns)
    fig = px.histogram(df, x=num_option, opacity=0.75)
    fig.update_layout(bargap=0.2, uniformtext_minsize=12, uniformtext_mode='hide')
    st.plotly_chart(fig, use_container_width=True)
with col2:
    cat_option = st.selectbox("Select Distribution of a Categorical Variable", category_columns)
    fig = px.histogram(df, x=cat_option)
    fig.update_layout(bargap=0.2)
    st.plotly_chart(fig, use_container_width=True)
st.divider()

if st.toggle("Bivariate Analysis"):
    st.markdown('#### Bivariate Analysis')
    st.write("Distribution of the Selected Columns")
    col3, col4 = st.columns(2)
    with col3:
        num_option1 = st.selectbox("Select Numerical Variable", numeric_columns)
    with col4:
        numeric_columns_x = numeric_df.drop(columns=num_option1).columns.tolist()
        num_option2 = st.selectbox("Select another Numerical Variable", numeric_columns_x)
       
    bi_fig = px.histogram(df, x=num_option2, y=num_option1, hover_data=df.columns)

    ### Visualization
    st.plotly_chart(bi_fig, use_container_width=True)
    st.divider()
    
if st.toggle('Multi-Variate Analysis'):
    st.markdown('#### Multi-Variate Analysis')
    st.write("Distribution of the Selected Columns")
    col5, col6, col7 = st.columns(3)
    with col5:
        num_optionA = st.selectbox("Select Numerical Variable", numeric_columns, key='selectboxA')
    with col6:
        numeric_columns_x = numeric_df.drop(columns=num_option1).columns.tolist()
        num_optionB = st.selectbox("Select another Numerical Variable", numeric_columns_x, key='selectboxB')
    with col7:
        cat_option1 = st.selectbox("Select a Categorical Identifier", category_columns)

    multi_fig = px.histogram(df, x=num_optionB, y=num_optionA, color=cat_option1,
                    marginal="box",  # or violin, rug
                    hover_data=df.columns)

    ### Visualization
    st.plotly_chart(multi_fig, use_container_width=True)
    st.divider()

st.subheader("Data Page")
st.warning("Check the **Editable Dataframes** option on the side widget to enable you change your values")


### Option to edit data
editableStatus = {0: "No", 1: "Yes"}
if st.sidebar.checkbox("Would you like to edit your data"):
    edit_df = st.data_editor(df, use_container_width=True)
    editableStatus = editableStatus[1]
else:
    st.dataframe(df, use_container_width=True)
    editableStatus = editableStatus[0]

st.sidebar.divider()

s_Col1, s_Col2, s_Col3 = st.sidebar.columns(3)
with s_Col1:
    st.markdown("### DATA SHAPE")
    st.write(shape)

with s_Col2:
    st.markdown("### EDITABLE STATUS")
    st.write(editableStatus)

with s_Col3:
    st.markdown("### NULL VALUES")
    st.write(null_values)

st.sidebar.divider()
st.sidebar.info("Made with ❤ by the AfroLogicInsect")
