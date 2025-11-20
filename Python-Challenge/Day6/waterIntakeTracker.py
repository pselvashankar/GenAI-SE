import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import streamlit as st
import os

# --- Configuration Constants ---
FILE_PATH = 'hydration_log.csv'
DAILY_GOAL_ML = 3000
DAILY_GOAL_L = DAILY_GOAL_ML / 1000

# --- Helper Function for Data Management ---

@st.cache_data(show_spinner="Loading hydration data...")
def _load_data():
    """
    Loads the hydration log from the CSV file, or creates a new empty DataFrame 
    if the file does not exist. Caching ensures fast reloads.
    """
    try:
        # Load the existing data
        df = pd.read_csv(FILE_PATH)
    except FileNotFoundError:
        # Create a new, empty DataFrame with the required columns
        df = pd.DataFrame(columns=['Date', 'Intake_ml'])
    
    # Ensure Intake_ml is numeric and handle potential NaN/missing data
    df['Intake_ml'] = pd.to_numeric(df['Intake_ml'], errors='coerce').fillna(0).astype(int)
    
    # Convert Date column to datetime objects
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    return df

def _save_data(df):
    """Saves the current DataFrame back to the CSV file."""
    df.to_csv(FILE_PATH, index=False)

# --- Core Tracking Functions ---

def log_intake(amount_ml: int):
    """
    Logs the water intake and updates the CSV file.
    Clears the Streamlit cache to force a UI refresh with new data.
    """
    if amount_ml <= 0:
        st.error("Intake amount must be positive.")
        return

    df = _load_data()
    today_str = datetime.now().strftime('%Y-%m-%d')
    today_date = datetime.now().date()
    
    # Use pandas to find or create the current day's entry
    if today_str in df['Date'].dt.strftime('%Y-%m-%d').values:
        # Update existing entry
        df.loc[df['Date'].dt.strftime('%Y-%m-%d') == today_str, 'Intake_ml'] += amount_ml
    else:
        # Create a new entry
        new_row = pd.DataFrame([{'Date': today_date, 'Intake_ml': amount_ml}])
        df = pd.concat([df, new_row], ignore_index=True)

    _save_data(df)
    
    # IMPORTANT: Clear the cache so the app re-runs and loads the new data
    st.cache_data.clear()
    st.toast(f"✅ Logged {amount_ml} ml successfully!")

def get_current_progress(df):
    """
    Calculates the current intake and remaining amount for today.
    """
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    # Get today's intake, default to 0 if no entry exists
    today_intake = df.loc[df['Date'].dt.strftime('%Y-%m-%d') == today_str, 'Intake_ml'].sum()
    
    remaining_ml = max(0, DAILY_GOAL_ML - today_intake)
    
    return today_intake, remaining_ml

def plot_weekly_hydration(df):
    """
    Generates a matplotlib bar chart for the last 7 unique days.
    Generates mock data if the log is insufficient. Returns the figure object.
    """
    # Aggregate intake by date to ensure one entry per day
    daily_summary = df.groupby(df['Date'].dt.date)['Intake_ml'].sum().reset_index()
    daily_summary.rename(columns={'Date': 'Date_Only'}, inplace=True)
    
    # Sort and take the last 7 unique days
    daily_summary = daily_summary.sort_values(by='Date_Only', ascending=False).head(7)
    
    # --- Mock Data Generation (Requirement) ---
    if len(daily_summary) < 7:
        # Create a list of the last 7 dates (date objects)
        last_seven_dates = [datetime.now().date() - timedelta(days=i) for i in range(6, -1, -1)]
        
        mock_data = pd.DataFrame({'Date_Only': last_seven_dates})
        
        # Merge existing data with the full 7-day range
        daily_summary = pd.merge(mock_data, daily_summary, on='Date_Only', how='left').fillna(0)
        daily_summary['Intake_ml'] = daily_summary['Intake_ml'].astype(int)
        
    # Final sort by date for plotting
    daily_summary = daily_summary.sort_values(by='Date_Only')
    
    # Prepare data for plotting
    dates = daily_summary['Date_Only']
    intake_liters = daily_summary['Intake_ml'] / 1000.0

    # --- Plotting ---
    # REDUCING FIGURE SIZE FROM (10, 5) TO (7, 4)
    fig, ax = plt.subplots(figsize=(7, 2))
    
    # Bar chart
    ax.bar(dates, intake_liters, color='#3498db', alpha=0.8, label="Intake")
    
    # Goal line (3.0 L)
    ax.axhline(DAILY_GOAL_L, color='red', linestyle='--', linewidth=1.5, label=f'Goal ({DAILY_GOAL_L:.1f} L)')
    
    # Customizing the plot
    ax.set_title("Weekly Water Intake (Last 7 Days)", fontsize=14, fontweight='bold')
    ax.set_xlabel("Day of the Week", fontsize=10)
    ax.set_ylabel("Water Intake (Liters)", fontsize=10)
    
    # Format X-axis to show short day names (e.g., 'Mon')
    # Use pandas datetime index for easier formatting
    ax.set_xticks(dates)
    ax.set_xticklabels([date.strftime('%a') for date in dates], rotation=0)
    
    ax.legend(fontsize=8)
    ax.grid(axis='y', linestyle=':', alpha=0.7)
    plt.tight_layout()
    
    # Return the figure object instead of calling plt.show()
    return fig

# --- Streamlit Application Layout ---

def app_main():
    """Main function to run the Streamlit app."""
    st.set_page_config(
        page_title="💧 Water Intake Tracker",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("💧 Daily Hydration Tracker")
    st.markdown("Log your water intake and visualize your progress toward the **3.0 L** daily goal.")

    # Load data once (cached)
    df = _load_data()
    today_intake, remaining_ml = get_current_progress(df)

    # --- Sidebar for Input ---
    with st.sidebar:
        st.header("Log Intake")
        st.markdown("Enter the amount of water you just drank (in ml).")
        
        # Use a form to group input and button, enabling a cleaner state reset
        with st.form("intake_form"):
            intake_amount = st.number_input(
                "Amount (ml)", 
                min_value=1, 
                value=250, 
                step=50,
                help="Common sizes: 250ml, 500ml, 750ml"
            )
            submitted = st.form_submit_button("Add Water Log")
            
            if submitted:
                log_intake(intake_amount)
                # After logging, the app will rerun, updating the main page content

        st.markdown("---")
        st.info(f"Today's Date: **{datetime.now().strftime('%Y-%m-%d')}**")


    # --- Main Content: Progress Metrics ---
    
    col1, col2, col3 = st.columns(3)
    
    # Determine the color and icon for the progress metric
    progress_color = "inverse" if today_intake >= DAILY_GOAL_ML else "normal"

    with col1:
        st.metric(
            label="Daily Goal", 
            value=f"{DAILY_GOAL_L:.1f} L", 
            delta_color="off", 
            help="Your target water consumption."
        )

    with col2:
        st.metric(
            label="Logged Today", 
            value=f"{today_intake} ml",
            delta=f"{today_intake / 1000:.2f} L",
            delta_color="off"
        )

    with col3:
        if remaining_ml > 0:
            st.metric(
                label="Remaining Until Goal", 
                value=f"{remaining_ml} ml", 
                delta_color="inverse", 
                delta=f"-{remaining_ml / 1000:.2f} L"
            )
        else:
            st.balloons()
            st.metric(
                label="Status", 
                value="GOAL MET! 🏆", 
                delta=f"Excess: {abs(remaining_ml) / 1000:.2f} L",
                delta_color="off"
            )

    st.markdown("---")

    # --- Main Content: Weekly Chart ---
    st.header("Weekly Hydration Overview")
    
    # Generate and display the plot
    try:
        fig = plot_weekly_hydration(df)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Could not generate plot: {e}")

if __name__ == "__main__":
    app_main()