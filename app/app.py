import streamlit as st
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots

# Load the dataset
df=pd.read_csv('..data/VideoGamesSales.csv')
st.set_page_config(page_title="Video Games Sales Analysis",page_icon=":bar_chart:",layout="wide")

st.markdown("""
<style>

/* Sidebar widget border */
section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stMultiSelect > div > div,
section[data-testid="stSidebar"] .stDateInput > div > div,
section[data-testid="stSidebar"] .stNumberInput > div > div {

    border: 1px solid #1f77ff !important;   /* blue outline */
    border-radius: 8px !important;
}

/* On hover */
section[data-testid="stSidebar"] .stSelectbox > div > div:hover,
section[data-testid="stSidebar"] .stMultiSelect > div > div:hover {
    border: 1px solid #3b82f6 !important;
}

/* On focus */
section[data-testid="stSidebar"] .stSelectbox > div > div:focus-within,
section[data-testid="stSidebar"] .stMultiSelect > div > div:focus-within {
    border: 1px solid #60a5fa !important;
    box-shadow: 0 0 5px #1f77ff !important;
}

 
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* Apply to ALL horizontal lines */
hr, div[data-testid="stMarkdownContainer"] hr {
    border: none !important;
    height: 2px !important;
    background: linear-gradient(to right, transparent, #1f77ff, transparent) !important;
    margin: 15px 0 !important;
}

/* Also target Streamlit divider if used */
div[data-testid="stDivider"] {
    background: linear-gradient(to right, transparent, #1f77ff, transparent) !important;
    height: 2px !important;
}

</style>
""", unsafe_allow_html=True)


#sidebar 1

st.sidebar.header("Filter Options")
regions=list(df['Region'].unique())
region=st.sidebar.multiselect("Select Region:",options=regions,default=regions)

#sidebar 2
countrys=list(df['Country'].unique())
country =st.sidebar.multiselect("Select Country:",options=countrys,default=countrys)

#sidebar 3
#years=mn.df['Year'].unique()
#year=st.sidebar.multiselect("Select Year:",options=years,default=years)

#Sidebar 4  
years = list(df['Year'].unique())

def toggle_select_all():
    if st.session_state.select_all:
        st.session_state.year_multiselect = years
    else:
        st.session_state.year_multiselect = []

st.sidebar.checkbox("Select All", key="select_all", on_change=toggle_select_all)

syear = st.sidebar.multiselect(
    "Select Year:",
    options=years,
    key="year_multiselect",
    default=years
)

df_selection = df.query(
    "Region == @region & Country == @country & Year == @syear"
)


#--------------------------------
#mainpage
st.title(":bar_chart: Video Games Sales Analysis")


#top KPIs
total_global_sales=int(df_selection['Global Sales'].sum())
average_global_sales=round(df_selection['Global Sales'].mean(),2)
total_national_sales=int(df_selection['National Sales'].sum())
average_national_sales=round(df_selection['National Sales'].mean(),2)
col1,col2,col3,col4=st.columns(4)
col1.metric("Total Global Sales",f"US ${total_global_sales:,}")
col2.metric("Average Global Sales",f"US ${average_global_sales:,}")     
col3.metric("Total National Sales",f"US ${total_national_sales:,}")
col4.metric("Average National Sales",f"US ${average_national_sales:,}")
st.markdown("---")


#creating a bar chart region or country vise sales
# nasales=df['National Sales'].sum()
# national_sales=df.groupby(['Region'])['National Sales'].sum().reset_index()
# fig=px.bar(national_sales,x='Region',y='National Sales')
# fig.update_layout(plot_bgcolor="white",xaxis=dict(showgrid=False))
# st.plotly_chart(fig,use_container_width=True)

#creating a bar chart region or country vise sales
national_sales = (df_selection.groupby('Region')['National Sales'].sum().reset_index())

fig = px.bar(national_sales,x='Region',y='National Sales',title="<b>National Sales by Region</b>",)


fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",xaxis=dict(showgrid=False),title={"x":0.5})
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
#creating a pie chart for sales by region
sales=df.groupby(['Country'])[['National Sales','Global Sales']].sum().reset_index()
country=sales['Country']
national_sales=sales['National Sales']
global_sales=sales['Global Sales']

fig=make_subplots(rows=1,cols=2,subplot_titles=["National Sales by Country","Global Sales by Country"],specs=[[{"type":"domain"},{"type":"domain"}]])

fig1 = px.pie(sales, values=national_sales, names=country, title='<b>National Sales by Country</b>',
             color_discrete_sequence=px.colors.sequential.RdBu) 

fig2 = px.pie(sales, values=global_sales, names=country, title='<b>Global Sales by Country</b>',
             color_discrete_sequence=px.colors.sequential.RdBu) 
fig.add_trace(fig1.data[0], row=1, col=1)
fig.add_trace(fig2.data[0], row=1, col=2)
fig.update_layout(title_text="<b>Sales Distribution by Country</b>", title={"x":0.5}, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.divider()


#creating a line chart for genre wise global profits
genre_sales=df_selection.groupby(['Genre'])['Global Sales'].sum().reset_index()
fig=px.bar(genre_sales,x='Genre',y='Global Sales',title="<b>Global Sales by Genre</b>")
fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",xaxis=dict(showgrid=False),title={"x":0.5})
st.plotly_chart(fig, use_container_width=True)
st.divider()

st.markdown("""
<h3 style='text-align: center;'>
Video Games Sales Table
</h3>
""", unsafe_allow_html=True)

st.dataframe(df, use_container_width=True)
