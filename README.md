# Electricity Analytics Dashboard

A comprehensive Streamlit dashboard for analyzing electricity consumption, pricing, and environmental factors.

## Project Structure

The application has been refactored into a modular structure for better maintainability:

### Core Modules

- **`app.py`** - Main application entry point
- **`data_loader.py`** - Data loading and processing functions
- **`ui_components.py`** - UI components, styling, and layout functions
- **`chart_utils.py`** - Chart creation and visualization logic
- **`metrics_calculator.py`** - Statistical calculations and metrics
- **`sidebar_controls.py`** - Sidebar configuration and user controls

### Data Files

- **`data/Electricity_consumption_2015-2025.csv`** - Electricity consumption data
- **`data/Electricity_price_2015-2025.csv`** - Electricity pricing data

## Features

- 📊 Interactive data visualization with multiple chart types
- 📈 Comprehensive metrics and statistics
- 🎨 Custom styling and responsive design
- 📅 Flexible date range selection
- 🔍 Correlation analysis and insights
- 📋 Detailed data views with filtering options

## Usage

1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `streamlit run app.py`
3. Use the sidebar controls to customize your analysis
4. Explore different chart types and metrics

## Module Responsibilities

- **Data Loading**: Handles CSV file loading, data cleaning, and preprocessing
- **UI Components**: Manages styling, headers, and reusable UI elements
- **Chart Utils**: Creates all visualizations (line, area, bar charts, heatmaps)
- **Metrics Calculator**: Performs statistical calculations and metric computations
- **Sidebar Controls**: Manages user input controls and configuration
- **Main App**: Orchestrates the application flow and module interactions

This modular structure makes the codebase more maintainable, testable, and easier to extend with new features.

## Overall Statistics Calculations

The dashboard displays comprehensive statistics for the selected time period. Here's how each metric is calculated:

### 🔋 Energy Consumption Section

**Total Consumption**
- **Calculation**: `sum(Consumption (kWh))` for all hours in selected period
- **Description**: Sum of all hourly electricity consumption values

**Daily Average**
- **Calculation**: `total_consumption / number_of_days_in_period`
- **Description**: Average daily consumption across the selected period

**Peak Consumption** (shown as delta)
- **Calculation**: `max(Consumption (kWh))`
- **Description**: Highest single hourly consumption value in the period

### 💰 Financial Impact Section

**Total Bill**
- **Calculation**: `sum(Bill (€))` for all hours in selected period
- **Description**: Total electricity cost for the selected period
- **Note**: Each hourly bill = `Consumption × (Price/100)` since price is in cents
- **Negative Values**: When prices are negative, bills become negative (customer receives credit)

**Daily Bill Average** (shown as delta)
- **Calculation**: `total_bill / number_of_days_in_period`
- **Description**: Average daily electricity cost

**Avg Price**
- **Calculation**: `mean(Price (cents/kWh))`
- **Description**: Average electricity price across all hours
- **Negative Values**: Can be negative when there's excess electricity production (renewable energy)

**Price Volatility** (shown as delta)
- **Calculation**: `std(Price (cents/kWh))`
- **Description**: Standard deviation showing price variability

### 🌡️ Environmental Section

**Avg Temperature**
- **Calculation**: `mean(Temperature (°C))`
- **Description**: Average temperature across all hours

**Temperature Range** (shown as delta)
- **Calculation**: `max(Temperature) - min(Temperature)`
- **Description**: Difference between highest and lowest temperatures

**Temp Impact**
- **Calculation**: Categorical classification based on average temperature and seasonal variation
- **Finnish Climate Logic** (Oulu-specific):
  - **Extreme Cold (< -15°C)**: "Extreme Cold (High Heating)" - Significant electricity demand for heating
  - **Very Cold (-15°C to -5°C)**: "Very Cold (High Heating)" - High heating requirements
  - **Cold (-5°C to 5°C)**: "Cold (Moderate Heating)" - Moderate heating needs
  - **Cool (5°C to 15°C)**: "Cool (Low Heating)" - Low heating requirements
  - **Mild (15°C to 25°C)**: "Mild (Minimal Heating)" - Minimal heating needed
  - **Warm (> 25°C)**: "Warm (No Heating)" - No heating required
- **Seasonal Variation**: Added based on temperature range:
  - "High Seasonal Variation" if range > 25°C
  - "Moderate Variation" if range > 15°C
  - "Low Variation" if range ≤ 15°C

### 📈 Efficiency Section

**Efficiency Score**
- **Calculation**: `daily_avg_consumption / avg_price` (if avg_price > 0)
- **Description**: Custom metric showing consumption efficiency relative to price
- **Interpretation**: Higher values indicate better efficiency

**Data Points**
- **Calculation**: `count(hourly_data_points)`
- **Description**: Total number of hourly data points in selected period

**Data Points in Days** (shown as delta)
- **Calculation**: `data_points / 24`
- **Description**: Converts hourly data points to equivalent days

### Key Notes

- All calculations are based on the filtered dataset for the selected date range
- Price handling: Prices are in cents, so bills are calculated by dividing by 100
- Time-based calculations use the actual date range span, not just data point count
- Includes error handling for edge cases (e.g., division by zero)
- Deltas provide additional context like volatility, peaks, and daily averages
