import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Streamlit app
st.set_page_config(page_title="Redbus Data Scraping", layout="wide")
st.title(":bus: :orange[**Redbus Data Scraping with Selenium & Dynamic Filtering**]")

# Sidebar with project information
with st.sidebar: 
    st.markdown("### :green_book: :green[**About**]")
    st.markdown('''
    This project aims to streamline the collection and analysis of bus travel data.
    Using **:blue[Selenium]** for automated data extraction from Redbus, it gathers details like routes, schedules, prices, and seat availability.
    This initiative helps improve operational efficiency and strategic planning in the transportation industry.
    ''')
    # Additional notes or instructions
    st.markdown("### :memo: :green[**Additional Notes**]")
    st.markdown("For more details, please refer to the [Redbus website](https://www.redbus.in).")


# MySQL credentials
mysql_user = 'root'
mysql_password = '1234'
mysql_host = 'localhost'
mysql_port = '3306'
mysql_database = 'Redbus'

# Create a connection to the MySQL database
engine = create_engine(f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}')

# Fetch data from the database
q1 = '''SELECT * FROM redbus_table'''
df_all = pd.read_sql(q1, engine)

# Main content layout
# st.markdown("### **:orange[Filter Options]**")
with st.container():
    col1, col2, col3 = st.columns(3)

    # Route filter 
    with col1:
        route_options = df_all['route'].unique()
        selected_route = st.selectbox('Select a Route:', route_options, index=None, placeholder='select a route')

    # Bus type filter
    q2 = '''SELECT * FROM redbus_table WHERE route = %s'''
    df_route = pd.read_sql(q2, engine, params=(selected_route,))
    with col2:
        bustype_options = df_route['Bus_type'].unique()
        selected_bustype = st.selectbox('Select a Bus Type:', bustype_options, index=None, placeholder='select a bustype')

    # Price filter
    q3 = '''SELECT * FROM redbus_table WHERE route = %s AND Bus_type = %s'''
    df_filtered = pd.read_sql(q3, engine, params=(selected_route, selected_bustype))
    with col3:
        price_options = df_filtered['Prices'].unique()
        selected_price = st.selectbox('Select a Price Range:', price_options, index=None, placeholder='select a price')

# Search button
if st.button('Search'):
    # Display filtered data
    st.markdown("### **:green[Filtered Bus Data]**")
    st.markdown(f"**Displaying data for:** *{selected_route}*, *{selected_bustype}*, *{selected_price}*")
    st.dataframe(df_filtered)

    # Download button for filtered data
    csv = df_filtered.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_redbus_data.csv',
        mime='text/csv',
    )
