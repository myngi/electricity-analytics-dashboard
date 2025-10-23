"""
Data loading and processing module for the Electricity Analytics Dashboard.
Handles CSV file loading, data cleaning, and preprocessing.
"""

import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    """
    Load and process electricity consumption and price data.
    
    Returns:
        pd.DataFrame: Combined and processed data with all metrics
    """
    consumption_path = "data/Electricity_consumption_2015-2025.csv"
    price_path = "data/Electricity_price_2015-2025.csv"

    # Load consumption data
    try:
        df_cons = pd.read_csv(consumption_path)
        df_cons['time'] = pd.to_datetime(df_cons['time'])
        df_cons = df_cons.set_index('time')
    except FileNotFoundError:
        st.error(f"Error: '{consumption_path}' not found. Make sure it's in the 'data' folder.")
        return pd.DataFrame()

    # Load price data
    try:
        df_price = pd.read_csv(price_path, 
                               delimiter=";", 
                               decimal=",")
        # The format is Month/Day/Year
        df_price['timestamp'] = pd.to_datetime(df_price['timestamp'], format="%H:%M %m/%d/%Y")
        df_price = df_price.set_index('timestamp')
    except FileNotFoundError:
        st.error(f"Error: '{price_path}' not found. Make sure it's in the 'data' folder.")
        return pd.DataFrame()
    except ValueError as e:
        st.error(f"Error parsing dates in '{price_path}'. Please check the format.")
        st.error(e) # Print the specific error
        return pd.DataFrame()

    # Join the two dataframes on their time index
    df = df_cons.join(df_price)

    # Drop any rows with missing data
    df = df.dropna()

    # Calculate hourly bill (Price is in cents, so divide by 100 for Euros)
    df['Bill'] = df['kWh'] * (df['Price'] / 100)

    # Rename columns for clarity in the app
    df = df.rename(columns={
        'kWh': 'Consumption (kWh)',
        'Price': 'Price (cents/kWh)',
        'Temperature': 'Temperature (°C)',
        'Bill': 'Bill (€)'
    })
    
    return df


def filter_data_by_date_range(df, start_date, end_date):
    """
    Filter dataframe by date range.
    
    Args:
        df (pd.DataFrame): Input dataframe
        start_date (datetime.date): Start date
        end_date (datetime.date): End date
        
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    return df.loc[start_date.strftime('%Y-%m-%d'):end_date.strftime('%Y-%m-%d')]


def calculate_default_date_range(df):
    """
    Calculate default start and end dates for the "last whole month".
    
    Args:
        df (pd.DataFrame): Input dataframe with datetime index
        
    Returns:
        tuple: (default_start_date, default_end_date)
    """
    min_date = df.index.min().date()
    max_date = df.index.max().date()
    
    # Calculate default start/end dates for the "last whole month"
    max_date_pd = pd.to_datetime(max_date)
    # Find the first day of the month of the max date, then subtract one day to get the end of the previous month
    default_end_date_dt = max_date_pd.replace(day=1) - pd.Timedelta(days=1)
    # Find the first day of that previous month
    default_start_date_dt = default_end_date_dt.replace(day=1)

    # Ensure default start date is not before the minimum available date
    default_start_date = max(min_date, default_start_date_dt.date())
    # Ensure default end date is not after the max date
    default_end_date = min(max_date, default_end_date_dt.date())
    
    # Fallback: If calculated start date is after calculated end date (e.g., if data is too short)
    # then just use the full range.
    if default_start_date > default_end_date:
         default_start_date = min_date 
         default_end_date = max_date   
    
    return default_start_date, default_end_date
