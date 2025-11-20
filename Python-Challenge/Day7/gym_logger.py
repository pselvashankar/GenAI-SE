import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- Constants ---
FILE_NAME = 'workout_log.csv'
COLUMNS = ['Date', 'Exercise Name', 'Sets', 'Reps', 'Weight (kg)', 'Total Volume']

# --- Data Management Functions ---

def initialize_file():
    """
    Checks if the CSV exists. If not, creates it with the required headers.
    """
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(FILE_NAME, index=False)

def load_data():
    """
    Loads the workout data from CSV.
    Returns:
        pd.DataFrame: The workout log.
    """
    try:
        df = pd.read_csv(FILE_NAME)
        # Ensure Date column is actually datetime objects for sorting/plotting
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(columns=COLUMNS)

def save_workout(exercise, sets, reps, weight):
    """
    Calculates volume and saves a new entry to the CSV.
    """
    try:
        # Calculate Total Volume
        total_volume = sets * reps * weight
        current_date = datetime.now().date()

        new_entry = pd.DataFrame([{
            'Date': current_date,
            'Exercise Name': exercise,
            'Sets': sets,
            'Reps': reps,
            'Weight (kg)': weight,
            'Total Volume': total_volume
        }])

        # Load existing, append, and save
        # We use mode='a' and header=False to append, 
        # but pandas is safer reading whole file, appending, and rewriting to avoid corruption
        current_df = load_data()
        updated_df = pd.concat([current_df, new_entry], ignore_index=True)
        updated_df.to_csv(FILE_NAME, index=False)
        return True
    except Exception as e:
        st.error(f"Failed to save data: {e}")
        return False

# --- UI Functions ---

def render_log_page():
    """Renders the form to log a new workout."""
    st.header("📝 Log a Workout")
    
    with st.form("workout_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            exercise_name = st.text_input("Exercise Name", placeholder="e.g., Bench Press")
            weight = st.number_input("Weight (kg)", min_value=0.0, step=0.5, format="%.1f")
        
        with col2:
            sets = st.number_input("Sets", min_value=1, step=1, value=3)
            reps = st.number_input("Reps", min_value=1, step=1, value=10)

        submitted = st.form_submit_button("Save Entry")

        if submitted:
            if not exercise_name.strip():
                st.warning("Please enter an exercise name.")
            else:
                success = save_workout(exercise_name.strip().title(), sets, reps, weight)
                if success:
                    st.success(f"Logged: {exercise_name} - {sets}x{reps} @ {weight}kg")

def render_history_page():
    """Renders the last 5 entries table."""
    st.header("📜 Workout History")
    
    df = load_data()
    
    if df.empty:
        st.info("No logs found yet. Go to 'Log Workout' to add some data!")
    else:
        st.subheader("Last 5 Entries")
        # Sort by date descending to show newest first, then take head(5)
        # Or just tail(5) if we assume append order. Let's invert the tail.
        recent_df = df.tail(5).iloc[::-1] 
        st.table(recent_df)

        with st.expander("See Full History"):
            st.dataframe(df)

def render_visualization_page():
    """Renders the Matplotlib chart for progress tracking."""
    st.header("📈 Progress Visualizer")
    
    df = load_data()
    
    if df.empty:
        st.info("No data to visualize yet.")
        return

    # Get unique exercises for the dropdown
    unique_exercises = df['Exercise Name'].unique()
    selected_exercise = st.selectbox("Select Exercise to View", unique_exercises)

    if selected_exercise:
        # Filter data
        filtered_df = df[df['Exercise Name'] == selected_exercise].sort_values(by='Date')

        if filtered_df.empty:
            st.warning("No data for this exercise.")
        else:
            # Matplotlib Plotting
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Plot Date vs Total Volume
            ax.plot(filtered_df['Date'], filtered_df['Total Volume'], marker='o', linestyle='-', color='#4CAF50')
            
            # Formatting
            ax.set_title(f"Volume Progress: {selected_exercise}", fontsize=14)
            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel("Total Volume (kg)", fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Format Date on X-Axis
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            fig.autofmt_xdate() # Rotate dates to fit

            # Render plot in Streamlit
            st.pyplot(fig)
            
            # specific stats
            max_vol = filtered_df['Total Volume'].max()
            st.metric(label="All-time Max Volume", value=f"{max_vol} kg")

# --- Main Application Loop ---

def main():
    st.set_page_config(page_title="Gym Logger", page_icon="🏋️‍♂️")
    
    # Ensure CSV exists on startup
    initialize_file()

    st.title("🏋️‍♂️ Gym Workout Logger")

    # Sidebar Navigation
    menu_options = ["Log Workout", "View History", "Visualize Progress"]
    choice = st.sidebar.radio("Menu", menu_options)

    # Routing
    if choice == "Log Workout":
        render_log_page()
    elif choice == "View History":
        render_history_page()
    elif choice == "Visualize Progress":
        render_visualization_page()

if __name__ == "__main__":
    main()