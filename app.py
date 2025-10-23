"""
Electricity Analytics Dashboard - Main Application
"""

import streamlit as st
import pandas as pd
import altair as alt

# Import our custom modules
from data_loader import load_data, filter_data_by_date_range
from ui_components import (
    apply_custom_css, render_main_header, render_section_header, 
    render_footer, render_error_message, render_data_viewer
)
from sidebar_controls import render_sidebar_controls
from metrics_calculator import (
    calculate_overall_metrics, calculate_quick_stats, 
    calculate_key_statistics, calculate_correlations, render_metrics_display
)
from chart_utils import create_chart, create_correlation_heatmap

# Set page configuration with custom styling
st.set_page_config(
    page_title="⚡ Electricity Analytics Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
apply_custom_css()

# Load the data
df = load_data()

if not df.empty:
    # Render main header
    render_main_header()

    # Render sidebar controls and get user selections
    user_selections = render_sidebar_controls(df)
    start_date = user_selections['start_date']
    end_date = user_selections['end_date']
    group_by = user_selections['group_by']
    chart_type = user_selections['chart_type']
    metric_to_display = user_selections['metric_to_display']
    show_trends = user_selections['show_trends']

    # Handle invalid date range
    if start_date > end_date:
        st.error("⚠️ Error: End date must be after start date.")
    else:
        # Filter data based on date range
        df_filtered = filter_data_by_date_range(df, start_date, end_date)

        # Display the overall metrics with enhanced styling
        render_section_header(f"📊 Overall Statistics ({start_date} to {end_date})")
        
        if df_filtered.empty:
            st.warning("No data available for the selected date range.")
        else:
            # Calculate and display metrics
            metrics = calculate_overall_metrics(df_filtered, start_date, end_date)
            render_metrics_display(metrics, df_filtered)

            # Create and display chart
            render_section_header(f"📈 {group_by} Trends & Analysis")
            
            chart = create_chart(df_filtered, group_by, chart_type, metric_to_display, show_trends)
            st.altair_chart(chart, use_container_width=True)

            # Additional insights and analysis
            render_section_header("🔍 Additional Insights & Analysis")

            # Create insights columns
            insight_col1, insight_col2 = st.columns(2)

            with insight_col1:
                st.markdown("#### 📊 Correlation Analysis")
                # Calculate correlations
                corr_chart = create_correlation_heatmap(df_filtered)
                st.altair_chart(corr_chart, use_container_width=True)

            with insight_col2:
                st.markdown("#### 📈 Key Statistics")
                
                # Calculate key statistics
                stats_df = calculate_key_statistics(df_filtered, metrics['efficiency_score'])
                st.dataframe(stats_df, use_container_width=True)

            # Enhanced data table with better styling, now collapsible
            render_data_viewer(df_filtered)

            # Footer with additional information
            render_footer()

else:
    # Handle data loading failure
    render_error_message()