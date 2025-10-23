"""
Metrics calculation and statistics module for the Electricity Analytics Dashboard.
Handles all statistical calculations and metric computations.
"""

import pandas as pd


def calculate_overall_metrics(df_filtered, start_date, end_date):
    """
    Calculate overall statistics for the selected period.
    
    Args:
        df_filtered (pd.DataFrame): Filtered dataframe
        start_date (datetime.date): Start date
        end_date (datetime.date): End date
        
    Returns:
        dict: Dictionary containing all calculated metrics
    """
    if df_filtered.empty:
        return {}
    
    total_consumption = df_filtered['Consumption (kWh)'].sum()
    total_bill = df_filtered['Bill (€)'].sum()
    avg_price = df_filtered['Price (cents/kWh)'].mean()
    avg_temp = df_filtered['Temperature (°C)'].mean()

    # Calculate additional metrics for better insights
    max_consumption = df_filtered['Consumption (kWh)'].max()
    min_consumption = df_filtered['Consumption (kWh)'].min()
    price_volatility = df_filtered['Price (cents/kWh)'].std()
    temp_range = df_filtered['Temperature (°C)'].max() - df_filtered['Temperature (°C)'].min()
    
    # Calculate daily average consumption more robustly
    num_days_in_filter = (end_date - start_date).days + 1
    daily_avg_consumption = total_consumption / num_days_in_filter
    
    # Calculate efficiency score
    efficiency_score = (daily_avg_consumption / avg_price) if avg_price > 0 else 0
    
    return {
        'total_consumption': total_consumption,
        'total_bill': total_bill,
        'avg_price': avg_price,
        'avg_temp': avg_temp,
        'max_consumption': max_consumption,
        'min_consumption': min_consumption,
        'price_volatility': price_volatility,
        'temp_range': temp_range,
        'daily_avg_consumption': daily_avg_consumption,
        'efficiency_score': efficiency_score,
        'num_days_in_filter': num_days_in_filter
    }


def calculate_quick_stats(df_filtered, start_date, end_date):
    """
    Calculate quick statistics for sidebar display.
    
    Args:
        df_filtered (pd.DataFrame): Filtered dataframe
        start_date (datetime.date): Start date
        end_date (datetime.date): End date
        
    Returns:
        dict: Dictionary containing quick stats
    """
    total_days = (end_date - start_date).days + 1
    
    if not df_filtered.empty:
        avg_consumption = df_filtered['Consumption (kWh)'].mean()
    else:
        avg_consumption = None
    
    return {
        'total_days': total_days,
        'avg_consumption': avg_consumption
    }


def calculate_key_statistics(df_filtered, efficiency_score):
    """
    Calculate key statistics for insights section.
    
    Args:
        df_filtered (pd.DataFrame): Filtered dataframe
        efficiency_score (float): Calculated efficiency score
        
    Returns:
        pd.DataFrame: DataFrame with key statistics
    """
    stats_data = {
        'Metric': ['Peak Consumption', 'Lowest Consumption', 'Price Range', 'Temp Range', 'Efficiency'],
        'Value': [
            f"{df_filtered['Consumption (kWh)'].max():.1f} kWh",
            f"{df_filtered['Consumption (kWh)'].min():.1f} kWh",
            f"{df_filtered['Price (cents/kWh)'].max() - df_filtered['Price (cents/kWh)'].min():.2f} cents",
            f"{df_filtered['Temperature (°C)'].max() - df_filtered['Temperature (°C)'].min():.1f}°C",
            f"{efficiency_score:.1f}"
        ]
    }
    
    return pd.DataFrame(stats_data)


def calculate_correlations(df_filtered):
    """
    Calculate correlation matrix for insights.
    
    Args:
        df_filtered (pd.DataFrame): Filtered dataframe
        
    Returns:
        pd.DataFrame: Correlation matrix
    """
    return df_filtered[['Consumption (kWh)', 'Price (cents/kWh)', 'Temperature (°C)', 'Bill (€)']].corr()


def render_metrics_display(metrics, df_filtered):
    """
    Render the metrics display in the main dashboard.
    
    Args:
        metrics (dict): Dictionary containing calculated metrics
        df_filtered (pd.DataFrame): Filtered dataframe for data point count
    """
    import streamlit as st
    
    # Enhanced metrics layout with icons and better styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("#### 🔋 Energy Consumption")
        st.metric("Total Consumption", f"{metrics['total_consumption']:,.0f} kWh", 
                  delta=f"Peak: {metrics['max_consumption']:.1f} kWh" if metrics['max_consumption'] > metrics['daily_avg_consumption'] else None)
        st.metric("Daily Average", f"{metrics['daily_avg_consumption']:.1f} kWh")
    
    with col2:
        st.markdown("#### 💰 Financial Impact")
        # Handle negative bills (when customer receives money)
        bill_text = f"€{metrics['total_bill']:,.2f}"
        if metrics['total_bill'] < 0:
            bill_text = f"€{metrics['total_bill']:,.2f} (Credit)"
        st.metric("Total Bill", bill_text, 
                  delta=f"€{metrics['total_bill']/metrics['num_days_in_filter']:.2f}/day")
        
        # Handle negative prices
        price_text = f"{metrics['avg_price']:,.2f} cents/kWh"
        if metrics['avg_price'] < 0:
            price_text = f"{metrics['avg_price']:,.2f} cents/kWh (Negative)"
        st.metric("Avg Price", price_text, 
                  delta=f"±{metrics['price_volatility']:.2f} std")
    
    with col3:
        st.markdown("#### 🌡️ Environmental")
        st.metric("Avg Temperature", f"{metrics['avg_temp']:.1f} °C", 
                  delta=f"Range: {metrics['temp_range']:.1f}°C")
        # Temperature impact classification for Finnish climate (Oulu)
        avg_temp = metrics['avg_temp']
        temp_range = metrics['temp_range']
        
        if avg_temp < -15:
            temp_impact = "Extreme Cold (High Heating)"
        elif avg_temp < -5:
            temp_impact = "Very Cold (High Heating)"
        elif avg_temp < 5:
            temp_impact = "Cold (Moderate Heating)"
        elif avg_temp < 15:
            temp_impact = "Cool (Low Heating)"
        elif avg_temp < 25:
            temp_impact = "Mild (Minimal Heating)"
        else:
            temp_impact = "Warm (No Heating)"
        
        # Add seasonal variation indicator
        if temp_range > 25:
            temp_variation = "High Seasonal Variation"
        elif temp_range > 15:
            temp_variation = "Moderate Variation"
        else:
            temp_variation = "Low Variation"
        
        # Display temperature impact in two rows
        st.markdown(f"**Temp Impact**")
        st.markdown(f"**{temp_impact}**")
        st.markdown(f"*{temp_variation}*")
    
    with col4:
        st.markdown("#### 📈 Efficiency")
        st.metric("Efficiency Score", f"{metrics['efficiency_score']:.1f}")
        st.metric("Data Points", f"{len(df_filtered):,}", 
                  delta=f"{len(df_filtered)/24:.1f} days")
