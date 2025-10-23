"""
Sidebar controls module for the Electricity Analytics Dashboard.
Handles all sidebar configuration and user input controls.
"""

import streamlit as st
import pandas as pd
from data_loader import calculate_default_date_range


def render_sidebar_controls(df):
    """
    Render all sidebar controls and return user selections.
    
    Args:
        df (pd.DataFrame): Main dataframe for date range calculations
        
    Returns:
        dict: Dictionary containing all user selections
    """
    with st.sidebar:
        st.markdown("### ⚙️ Dashboard Controls")
        st.markdown("---")

        # Get min and max dates from the data for the date input
        min_date = df.index.min().date()
        max_date = df.index.max().date()

        # Calculate default start/end dates for the "last whole month"
        default_start_date, default_end_date = calculate_default_date_range(df)

        # Date range selector
        st.markdown("#### 📅 Date Range")
        start_date = st.date_input("Start date", 
                                   value=default_start_date,
                                   min_value=min_date, 
                                   max_value=max_date,
                                   key="start_date")
        
        end_date = st.date_input("End date", 
                                 value=default_end_date,
                                 min_value=min_date, 
                                 max_value=max_date,
                                 key="end_date")

        st.markdown("---")
        
        # Grouping interval selector
        st.markdown("#### 📊 Visualization Settings")
        group_by = st.selectbox("Group data by", ["Daily", "Weekly", "Monthly"])
        
        # Chart type selector
        chart_type = st.selectbox("Chart type", ["Line Chart", "Area Chart", "Bar Chart"])

        # Metric selector for the chart
        metric_to_display = st.selectbox(
            "Select Metric to Display",
            ["Consumption (kWh)", "Bill (€)", "Price (cents/kWh)", "Temperature (°C)", "All (Faceted)"]
        )
        
        # Additional options
        st.markdown("#### 🎨 Display Options")
        show_trends = st.checkbox("Show trend lines", value=True)
        
        st.markdown("---")
        
        # Quick stats in sidebar
        st.markdown("#### 📈 Quick Stats")
        # Recalculate total_days based on the selected dates
        total_days = (end_date - start_date).days + 1
        st.metric("Selected Period", f"{total_days} days")
        
        if start_date <= end_date:
            # Use loc for date range slicing on DataFrames
            df_temp = df.loc[start_date.strftime('%Y-%m-%d'):end_date.strftime('%Y-%m-%d')]
            if not df_temp.empty:
                avg_consumption = df_temp['Consumption (kWh)'].mean()
                st.metric("Avg Daily Consumption", f"{avg_consumption:.2f} kWh")
            else:
                st.metric("Avg Daily Consumption", "N/A")

    return {
        'start_date': start_date,
        'end_date': end_date,
        'group_by': group_by,
        'chart_type': chart_type,
        'metric_to_display': metric_to_display,
        'show_trends': show_trends
    }
