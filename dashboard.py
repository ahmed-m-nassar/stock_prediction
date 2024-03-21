import os
import streamlit as st
import yfinance as yf
import altair as alt
import matplotlib.pyplot as plt
import pandas as pd
from src.utils.db_utils import connect_to_database , select_data

def get_latest_prediction(date) :
    connection = connect_to_database(os.environ.get("DB_URL"))
    result = select_data(connection,
                         'stocks_predictions',
                         columns=['date', 'prediction'],
                         where_clause=f"date = '{date}'")
    print(str(date))
    connection.close()
    # Check if there's any result
    if result:
        max_date, prediction = result[0]
        # Get the maximum date and prediction from your data source

        # Determine the prediction direction and color
        direction = "Down" if prediction == 0 else "Up"
        color = "red" if prediction == 0 else "green"

        # Write the prediction direction with colored text
        st.markdown(f"Closing price will go : <span style='color:{color}'>{direction}</span>", unsafe_allow_html=True)
    else:
        st.write("No data found.")
        
# Function to get historical data
def get_historical_data():
    # Fetch historical data for AAPL stock
    data = yf.download('AAPL', start='2023-01-01', progress=False)
    return data

# Function to get today's details and display them in Streamlit columns
def get_todays_details():
    # Fetch today's details for AAPL stock
    data = yf.download('AAPL', progress=False)
    today_details = data.iloc[-1]  # Selecting the last row as today's details

    # Display each piece of information in separate Streamlit columns
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    with col1:
        st.write("Date")
        st.write(today_details.name.strftime("%Y-%m-%d"))
    
    with col2:
        st.write("Open")
        st.write(round(today_details["Open"], 4 ))  # Round to 2 decimal places

    with col3:
        st.write("High")
        st.write(round(today_details["High"], 4 ))  # Round to 2 decimal places

    with col4:
        st.write("Low")
        st.write(round(today_details["Low"], 4 ))  # Round to 2 decimal places

    with col5:
        st.write("Close")
        st.write(round(today_details["Close"], 4 ))  # Round to 2 decimal places

    with col6:
        st.write("Volume")
        st.write(round(today_details["Volume"] ))  # Round to 2 decimal places

    with col7:
        st.write("Adj Close")
        st.write(round(today_details["Adj Close"], 4 ))  # Round to 2 decimal places
    return today_details.name.strftime("%Y-%m-%d")
        
# Function to display historical data
def display_historical_data():
    st.subheader('Historical Data for AAPL')
    historical_data = get_historical_data()

    # Resample data to daily frequency and reset index
    historical_data = historical_data.resample('D').ffill().reset_index()

    # Create Altair chart with adjusted opacity
    chart = alt.Chart(historical_data).mark_line(opacity=0.7).encode(
        x='Date:T',
        y='Adj Close:Q',
        tooltip=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
    ).properties(
        width=800,
        height=400
    ).interactive()

    # Display Altair chart
    st.altair_chart(chart)


# Function to display today's details
def display_todays_details( ):
    st.subheader("Today's Details for AAPL")
    today_date = get_todays_details()
    get_latest_prediction(today_date)

# Function to display price prediction
def display_price_prediction():
    st.subheader("Price Prediction")
    st.write("Work in progress...")  # Placeholder for the price prediction section
    
# Function to fetch data
def fetch_data():
    # Implement data fetching logic here
    pass

# Main function to run the Streamlit app
def main():
    st.title('AAPL Stock Analysis and Prediction')
    if st.button("Refresh Data"):
        message = fetch_data()
    

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Data :clipboard:", "Global Performance :weight_lifter:", "Local Performance :bicyclist:"])
    with tab1:
       # get_latest_prediction()
        display_todays_details()
        display_historical_data()
    with tab2:
        display_todays_details()
    with tab3:
        display_price_prediction()

if __name__ == "__main__":
    main()
