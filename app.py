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
import seaborn as sns
import matplotlib.pyplot as plt
import pyarrow
import plotly.express as px
import plotly.offline as py
import plotly.figure_factory as ff
import plotly.graph_objs as go

### Placeholder Data
df = pd.read_csv("./dta/sample_data.csv")

### Functions come here
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
numeric_df = df.select_dtypes(include=numerics)
numeric_columns = numeric_df.columns.tolist()
category_df = df.drop(columns=numeric_columns)
category_columns = category_df.columns.tolist()


def plot_value_counts(col_name, table=False, bar=False):
    values_count = pd.DataFrame(df[col_name].value_counts())
    values_count.columns = ['count']
    # convert the index column into a regular column.
    values_count[col_name] = [str(i) for i in values_count.index]
    # add a column with the percentage of each data point to the sum of all data points.
    values_count['percent'] = values_count['count'].div(values_count['count'].sum()).multiply(100).round(2)
    # change the order of the columns.
    values_count = values_count.reindex_axis([col_name, 'count', 'percent'], axis=1)
    values_count.reset_index(drop=True, inplace=True)

    if bar:
        # add a font size for annotations0 which is relevant to the length of the data points.
        font_size = 20 - (.25 * len(values_count[col_name]))

        trace0 = gobj.Bar(x=values_count[col_name], y=values_count['count'])
        data_ = gobj.Data([trace0])

        annotations0 = [dict(x=xi,
                             y=yi,
                             showarrow=False,
                             font={'size': font_size},
                             text="{:,}".format(yi),
                             xanchor='center',
                             yanchor='bottom')
                        for xi, yi, _ in values_count.values]

        annotations1 = [dict(x=xi,
                             y=yi / 2,
                             showarrow=False,
                             text="{}%".format(pi),
                             xanchor='center',
                             yanchor='center',
                             font={'color': 'yellow'})
                        for xi, yi, pi in values_count.values if pi > 10]

        annotations = annotations0 + annotations1

        layout = gobj.Layout(title=col_name.replace('_', ' ').capitalize(),
                             titlefont={'size': 50},
                             yaxis={'title': 'count'},
                             xaxis={'type': 'category'},
                             annotations=annotations)
        figure = gobj.Figure(data=data_, layout=layout)
        py.iplot(figure)

    if table:
        values_count['count'] = values_count['count'].apply(lambda d: "{:,}".format(d))
        table = ff.create_table(values_count, index_title="race")
        py.iplot(table)

    return values_count


### Page components come here
#### > Handles
st.sidebar.title("Page Handles")

uploaded_file = st.sidebar.file_uploader("Choose a File {.csv, .parquet}", type=["csv", "parquet"])

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

st.markdown('#### Bivariate Analysis')
st.write("Distribution of the Selected Columns")
col3, col4, col5 = st.columns(3)
with col3:
    num_option1 = st.selectbox("Select Numerical Variable", numeric_columns)

with col4:
    numeric_columns_x = numeric_df.drop(columns=num_option1).columns.tolist()
    num_option2 = st.selectbox("Select another Numerical Variable", numeric_columns_x)
with col5:
    cat_option1 = st.selectbox("Select a Categorical Identifier", category_columns)
fig = px.histogram(df, x=num_option2, y=num_option1, color=cat_option1,
                   marginal="box",  # or violin, rug
                   hover_data=df.columns)
st.plotly_chart(fig, use_container_width=True)
st.divider()

st.subheader("Data Page")
st.warning("Check the **Editable Dataframes** option on the side widget to enable you change your values")

### Option to edit data
Editable_Status = {0: "No", 1: "Yes"}
if st.sidebar.checkbox("Would you like to edit your data"):
    edit_df = st.experimental_data_editor(df, use_container_width=True)
    edit_df.to_csv('./dta/edit_data.csv')
    df = pd.read_csv("./dta/edit_data.csv")
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
