"""
Chart creation and visualization utilities for the Electricity Analytics Dashboard.
Handles all chart types and visualization logic.
"""

import pandas as pd
import altair as alt
import streamlit as st


def prepare_chart_data(df_filtered, group_by):
    """
    Prepare data for chart visualization by grouping and resampling.
    
    Args:
        df_filtered (pd.DataFrame): Filtered dataframe
        group_by (str): Grouping interval ('Daily', 'Weekly', 'Monthly')
        
    Returns:
        pd.DataFrame: Prepared chart data in long format
    """
    # Calculate grouped data for the chart
    group_map = {'Daily': 'D', 'Weekly': 'W', 'Monthly': 'MS'}
    rule = group_map[group_by]

    # Resample data
    df_grouped = df_filtered.resample(rule).agg({
        'Consumption (kWh)': 'sum',
        'Bill (€)': 'sum',
        'Price (cents/kWh)': 'mean',
        'Temperature (°C)': 'mean'
    })
    
    # Convert grouped data from wide to long format for Altair
    df_grouped.index.name = 'Date'
    df_chart_data = df_grouped.reset_index().melt('Date', var_name='Metric', value_name='Value')
    
    return df_chart_data


def filter_chart_data(df_chart_data, metric_to_display):
    """
    Filter chart data based on selected metric.
    
    Args:
        df_chart_data (pd.DataFrame): Chart data in long format
        metric_to_display (str): Selected metric to display
        
    Returns:
        pd.DataFrame: Filtered chart data
    """
    if metric_to_display != "All (Faceted)":
        return df_chart_data[df_chart_data['Metric'] == metric_to_display]
    else:
        return df_chart_data


def create_line_chart(df_chart, metric_to_display, show_trends):
    """
    Create line chart based on metric selection.
    
    Args:
        df_chart (pd.DataFrame): Chart data
        metric_to_display (str): Selected metric
        show_trends (bool): Whether to show trend lines
        
    Returns:
        alt.Chart: Configured line chart
    """
    # Create base line chart
    base_line_chart = alt.Chart(df_chart).mark_line(
        point=True, 
        strokeWidth=3,
        opacity=0.8
    ).encode(
        x=alt.X('Date:T', axis=alt.Axis(title='Date', titleFontSize=14, labelFontSize=12)),
        y=alt.Y('Value:Q', title=None),
        color=alt.Color('Metric:N', 
                      scale=alt.Scale(scheme='category20'),
                      legend=alt.Legend(title="Metrics", titleFontSize=14, labelFontSize=12)),
        tooltip=[
            alt.Tooltip('Date:T', title='Date', format='%Y-%m-%d'),
            alt.Tooltip('Metric:N', title='Metric'),
            alt.Tooltip('Value:Q', title='Value', format='.2f')
        ]
    ) 

    # Check if trends are needed and LAYER first
    if show_trends:
        trend = alt.Chart(df_chart).transform_regression(
            'Date', 'Value', groupby=['Metric']
        ).mark_line(
            color='red', 
            strokeDash=[5, 5], 
            opacity=0.5,
            strokeWidth=2
        ).encode(
            x='Date:T',
            y='Value:Q'
        )
        chart = base_line_chart + trend
    else:
        chart = base_line_chart

    # Apply facet CONDITIONALLY
    if metric_to_display == "All (Faceted)":
        chart = chart.facet(
            row=alt.Row('Metric:N', 
                        title=None, 
                        header=alt.Header(
                            labels=True, 
                            titleOrient="top", 
                            labelOrient="top",
                            labelFontSize=12,
                            labelColor='#333333'
                        )),
            data=df_chart
        ).resolve_scale(y='shared')

    return chart


def create_area_chart(df_chart, metric_to_display):
    """
    Create area chart.
    
    Args:
        df_chart (pd.DataFrame): Chart data
        metric_to_display (str): Selected metric
        
    Returns:
        alt.Chart: Configured area chart
    """
    # Area chart with gradient fills
    chart = alt.Chart(df_chart).mark_area(
        opacity=0.6,
        interpolate='monotone'
    ).encode(
        x=alt.X('Date:T', axis=alt.Axis(title='Date', titleFontSize=14, labelFontSize=12)),
        y=alt.Y('Value:Q', title=None),
        color=alt.Color('Metric:N', 
                      scale=alt.Scale(scheme='viridis'),
                      legend=alt.Legend(title="Metrics", titleFontSize=14, labelFontSize=12)),
        tooltip=[
            alt.Tooltip('Date:T', title='Date', format='%Y-%m-%d'),
            alt.Tooltip('Metric:N', title='Metric'),
            alt.Tooltip('Value:Q', title='Value', format='.2f')
        ]
    )
    
    # Apply facet CONDITIONALLY
    if metric_to_display == "All (Faceted)":
        chart = chart.facet(
            row=alt.Row('Metric:N', 
                        title=None, 
                        header=alt.Header(
                            labels=True, 
                            titleOrient="top", 
                            labelOrient="top",
                            labelFontSize=12
                        )),
            data=df_chart
        ).resolve_scale(y='shared')

    return chart


def create_bar_chart(df_chart, metric_to_display):
    """
    Create bar chart.
    
    Args:
        df_chart (pd.DataFrame): Chart data
        metric_to_display (str): Selected metric
        
    Returns:
        alt.Chart: Configured bar chart
    """
    # Bar chart for comparison
    chart = alt.Chart(df_chart).mark_bar(
        opacity=0.8,
        cornerRadius=4
    ).encode(
        x=alt.X('Date:T', axis=alt.Axis(title='Date', titleFontSize=14, labelFontSize=12)),
        y=alt.Y('Value:Q', title=None),
        color=alt.Color('Metric:N', 
                      scale=alt.Scale(scheme='set2'),
                      legend=alt.Legend(title="Metrics", titleFontSize=14, labelFontSize=12)),
        tooltip=[
            alt.Tooltip('Date:T', title='Date', format='%Y-%m-%d'),
            alt.Tooltip('Metric:N', title='Metric'),
            alt.Tooltip('Value:Q', title='Value', format='.2f')
        ]
    )
    
    # Apply facet CONDITIONALLY
    if metric_to_display == "All (Faceted)":
        chart = chart.facet(
            row=alt.Row('Metric:N', 
                        title=None, 
                        header=alt.Header(
                            labels=True, 
                            titleOrient="top", 
                            labelOrient="top",
                            labelFontSize=12
                        )),
            data=df_chart
        ).resolve_scale(y='shared')

    return chart


def create_correlation_heatmap(df_filtered):
    """
    Create correlation heatmap for insights.
    
    Args:
        df_filtered (pd.DataFrame): Filtered dataframe
        
    Returns:
        alt.Chart: Correlation heatmap chart
    """
    # Calculate correlations
    corr_data = df_filtered[['Consumption (kWh)', 'Price (cents/kWh)', 'Temperature (°C)', 'Bill (€)']].corr()
    
    # Create correlation heatmap
    corr_chart = alt.Chart(corr_data.reset_index().melt('index')).mark_rect().encode(
        x='index:N',
        y='variable:N',
        color=alt.Color('value:Q', scale=alt.Scale(scheme='redblue', domain=[-1, 1])),
        tooltip=['index:N', 'variable:N', 'value:Q']
    ).properties(
        width=300,
        height=300
    )
    
    return corr_chart


def create_chart(df_filtered, group_by, chart_type, metric_to_display, show_trends):
    """
    Main function to create charts based on user selections.
    
    Args:
        df_filtered (pd.DataFrame): Filtered dataframe
        group_by (str): Grouping interval
        chart_type (str): Type of chart to create
        metric_to_display (str): Selected metric
        show_trends (bool): Whether to show trend lines
        
    Returns:
        alt.Chart: Final configured chart
    """
    # Prepare chart data
    df_chart_data = prepare_chart_data(df_filtered, group_by)
    
    # Filter data based on metric selection
    df_chart = filter_chart_data(df_chart_data, metric_to_display)
    
    # Filter the chart data based on the sidebar selection
    if metric_to_display != "All (Faceted)":
        df_chart = df_chart[df_chart['Metric'] == metric_to_display]
    
    # Create chart based on type
    if chart_type == "Line Chart":
        chart = create_line_chart(df_chart, metric_to_display, show_trends)
    elif chart_type == "Area Chart":
        chart = create_area_chart(df_chart, metric_to_display)
    else:  # Bar Chart
        chart = create_bar_chart(df_chart, metric_to_display)
    
    # Apply final configurations
    final_chart = chart.configure(
        background='transparent'
    ).configure_view(
        strokeWidth=0
    )
    
    return final_chart
