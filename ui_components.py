"""
UI components and styling module for the Electricity Analytics Dashboard.
Contains custom CSS, headers, and reusable UI components.
"""

import streamlit as st


def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app."""
    st.markdown("""
    <style>
        /* Main theme colors */
        .main-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .main-header h1 {
            color: white;
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }
        
        .main-header p {
            color: rgba(255, 255, 255, 0.9);
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
        }
        
        /* Metric cards styling */
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
            margin: 0.5rem 0;
        }
        
        /* Section headers */
        .section-header {
            background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 2rem 0 1rem 0;
            font-size: 1.5rem;
            font-weight: 600;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Custom metric styling */
        [data-testid="metric-container"] {
            background: white;
            border: 1px solid #e0e0e0;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            border-left: 4px solid #667eea;
        }
        
        /* Hide Streamlit branding */
        /* #MainMenu {visibility: hidden;}  */
        footer {visibility: hidden;}
        /* header {visibility: hidden;} */
    </style>
    """, unsafe_allow_html=True)


def render_main_header():
    """Render the main dashboard header."""
    st.markdown("""
    <div class="main-header">
        <h1>⚡ Electricity Analytics Dashboard</h1>
        <p>Analysis of Energy Consumption, Pricing & Environmental Factors</p>
    </div>
    """, unsafe_allow_html=True)


def render_section_header(title):
    """
    Render a section header with custom styling.
    
    Args:
        title (str): The section title
    """
    st.markdown(f"""
    <div class="section-header">
        {title}
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    """Render the dashboard footer."""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>⚡ Electricity Analytics Dashboard | Powered by Streamlit & Altair</p>
        <p><small>Data Analysis & Visualization for Energy Consumption Insights</small></p>
    </div>
    """, unsafe_allow_html=True)


def render_error_message():
    """Render error message when data loading fails."""
    st.error("🔴 Data Loading Failed: The dashboard cannot be displayed.")
    st.warning(
        "Please make sure you have a folder named 'data' in the same directory as your 'app.py' file, "
        "and that it contains 'Electricity_consumption_2015-2025.csv' and 'Electricity_price_2015-2025.csv'."
    )
    st.info("Check the file path errors printed by the `load_data` function (they may be above this message) for more details.")


def render_data_viewer(df_filtered):
    """
    Render the detailed data view with collapsible expander.
    
    Args:
        df_filtered (pd.DataFrame): Filtered dataframe to display
    """
    with st.expander("📋 Detailed Data View", expanded=False):
        # Data table with enhanced features
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown("#### 📊 Raw Data Table")
        
        with col2:
            show_sample = st.checkbox("Show sample only", value=True)
        
        with col3:
            sample_size = st.slider("Sample size", 10, 1000, 100, 10)

        if show_sample:
            sample_data = df_filtered.head(sample_size)
            st.dataframe(
                sample_data.round(2),
                use_container_width=True,
                height=400
            )
        else:
            st.dataframe(
                df_filtered.round(2),
                use_container_width=True,
                height=400
            )

        # Summary statistics
        st.markdown("#### 📈 Summary Statistics")
        summary_stats = df_filtered.describe().round(2)
        st.dataframe(summary_stats, use_container_width=True)
