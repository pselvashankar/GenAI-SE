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
        current_df = load_data()
        updated_df = pd.concat([current_df, new_entry], ignore_index=True)
        updated_df.to_csv(FILE_NAME, index=False)
        return True
    except Exception as e:
        st.error(f"Failed to save data: {e}")
        return False

# --- UI Functions ---

def render_log_section():
    """Renders the form to log a new workout."""
    st.subheader("📝 Log a Workout")
    
    with st.container():
        with st.form("workout_form", clear_on_submit=True):
            c1, c2, c3, c4 = st.columns(4)
            
            with c1:
                exercise_name = st.text_input("Exercise", placeholder="e.g. Bench Press")
            with c2:
                weight = st.number_input("Weight (kg)", min_value=0.0, step=0.5, format="%.1f")
            with c3:
                sets = st.number_input("Sets", min_value=1, step=1, value=3)
            with c4:
                reps = st.number_input("Reps", min_value=1, step=1, value=10)

            submitted = st.form_submit_button("Add Entry", use_container_width=True)

            if submitted:
                if not exercise_name.strip():
                    st.warning("Please enter an exercise name.")
                else:
                    success = save_workout(exercise_name.strip().title(), sets, reps, weight)
                    if success:
                        st.success(f"Logged: {exercise_name} - {sets}x{reps} @ {weight}kg")

def render_history_section():
    """Renders the last 5 entries table."""
    st.subheader("📜 Recent History")
    
    df = load_data()
    
    if df.empty:
        st.info("No logs yet.")
    else:
        # Sort by date descending to show newest first
        recent_df = df.tail(5).iloc[::-1] 
        st.dataframe(recent_df, use_container_width=True, hide_index=True)

        with st.expander("See Full History"):
            st.dataframe(df, use_container_width=True)

def render_visualization_section():
    """Renders the Matplotlib chart for progress tracking."""
    st.subheader("📈 Progress Visualizer")
    
    df = load_data()
    
    if df.empty:
        st.info("Log some workouts to see charts!")
        return

    # Get unique exercises for the dropdown
    unique_exercises = df['Exercise Name'].unique()
    selected_exercise = st.selectbox("Select Exercise", unique_exercises)

    if selected_exercise:
        # Filter data
        filtered_df = df[df['Exercise Name'] == selected_exercise].sort_values(by='Date')

        if filtered_df.empty:
            st.warning("No data for this exercise.")
        else:
            # Matplotlib Plotting
            # Reduced size from (8, 4) to (6, 3)
            fig, ax = plt.subplots(figsize=(6, 3))
            
            # Plot Date vs Total Volume
            ax.plot(filtered_df['Date'], filtered_df['Total Volume'], marker='o', linestyle='-', color='#4CAF50', linewidth=2)
            
            # Formatting
            ax.set_title(f"Volume: {selected_exercise}", fontsize=10)
            ax.set_xlabel("Date", fontsize=8)
            ax.set_ylabel("Volume (kg)", fontsize=8)
            ax.tick_params(axis='both', which='major', labelsize=8)
            ax.grid(True, linestyle=':', alpha=0.6)
            
            # Fix Date Formatting on X-Axis
            # Use AutoDateLocator to intelligently pick ticks (prevents repetition on sparse data)
            locator = mdates.AutoDateLocator()
            formatter = mdates.ConciseDateFormatter(locator)
            
            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)
            
            fig.autofmt_xdate() 

            # Render plot in Streamlit
            st.pyplot(fig)

# --- Main Application Loop ---

def main():
    # Set layout to wide so we can put history and graph side-by-side
    st.set_page_config(page_title="Gym Logger", page_icon="🏋️‍♂️", layout="wide")
    
    # Custom CSS to remove top space and change background
    st.markdown("""
        <style>
            /* Reduce top padding */
            .block-container {
                padding-top: 1rem;
                padding-bottom: 1rem;
            }
            /* Change background color to a pleasant Alice Blue */
            .stApp {
                background-color: #F0F8FF;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Ensure CSV exists on startup
    initialize_file()

    st.title("🏋️‍♂️ Gym Workout Logger")
    st.markdown("---")

    # Top Section: Logging
    render_log_section()

    st.markdown("---")

    # Bottom Section: Dashboard (History + Viz)
    col1, col2 = st.columns([1, 1.5], gap="large")

    with col1:
        render_history_section()
    
    with col2:
        render_visualization_section()

if __name__ == "__main__":
    main()