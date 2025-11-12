import streamlit as st
import datetime
# PIL import is no longer strictly needed but kept as a habit from Tkinter conversion

# --- Configuration and Utility Functions ---

# Removed the get_greeting() function as it's no longer time-dependent.

def generate_greeting_message():
    """
    Called when the 'Generate Greeting' button is clicked.
    Handles validation and updates the greeting message in session state,
    using the specific Social Eagle Day 1 message.
    """
    first = st.session_state.first_name_input.strip()
    last = st.session_state.last_name_input.strip()
    age = int(st.session_state.age_slider)

    # Input validation
    if not first or not last:
        st.session_state.message_type = "error"
        st.session_state.message_content = "⚠️ Please enter **both** your First Name and Last Name to proceed."
        st.session_state.greeting_data = None
        return

    # Success: Compile result
    
    # --- STATIC GREETING MESSAGE REPLACEMENT ---
    challenge_greeting = "Welcome to Social Eagle Batch-3 Day 1 Python Challenge!"
    # -------------------------------------------
    
    st.session_state.message_type = "success"
    st.session_state.message_content = f"✅ Greeting successfully generated for {first}!"
    
    # Store data for display
    st.session_state.greeting_data = {
        "full_name": f"{first} {last}".upper(),
        "age_line": f"You are **{age}** years old.",
        "greeting_line": challenge_greeting, # Use the fixed message here
    }

# --- Page Configuration ---
st.set_page_config(
    page_title="Professional Greeting Generator",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize session state for persistent data
if 'greeting_data' not in st.session_state:
    st.session_state.greeting_data = None
if 'message_type' not in st.session_state:
    st.session_state.message_type = "info"
if 'message_content' not in st.session_state:
    st.session_state.message_content = "Enter your details in the sidebar and click the button to generate your personalized greeting."

# --- Sidebar Input Form ---
with st.sidebar:
    st.header("👤 Your Details")
    st.markdown("---")

    with st.form(key='user_form'):
        # 1. Name Inputs
        st.subheader("Names")
        
        # --- FIX APPLIED TO FIRST NAME INPUT ---
        st.text_input(
            label="First Name",
            key="first_name_input",
            placeholder="e.g., John",
            max_chars=50,
            # FIX: Use help for the submit instruction and collapse the label
            help="Press Enter inside the text box to easily submit the form.", 
            label_visibility='collapsed' 
        )
        
        # --- FIX APPLIED TO LAST NAME INPUT ---
        st.text_input(
            label="Last Name",
            key="last_name_input",
            placeholder="e.g., Doe",
            max_chars=50,
            # FIX: Use help for the submit instruction and collapse the label
            help="Press Enter inside the text box to easily submit the form.",
            label_visibility='collapsed'
        )
        
        st.markdown("---")

        # 2. Age Slider
        st.subheader("Age")
        st.slider(
            label="Select Age",
            min_value=5,
            max_value=100,
            value=25,
            step=1,
            key="age_slider",
            help="Drag to select your current age.",
        )

        st.markdown("---")

        # 3. Submit Button
        st.form_submit_button(
            label="Generate Greeting ✨",
            on_click=generate_greeting_message,
            type="primary",
            use_container_width=True
        )

    # Footer in the Sidebar
    st.markdown("---")
    st.caption(f"App by Social Eagle Batch-3 | {datetime.datetime.now().year}")

# --- Main Page Display (Header and Result) ---

# 1. Header (A clean title and subheader)
st.title("🦅 Social Eagle Challenge Greeting")
st.markdown("#### Personalized welcome for Day 1 participants.")
st.markdown("---")


# 2. Status/Error Message Display
if st.session_state.message_type == "error":
    st.error(st.session_state.message_content,icon="❌")
elif st.session_state.message_type == "success":
    st.success(st.session_state.message_content,icon="🎉")
else:
    st.info(st.session_state.message_content,icon="ℹ️")


# 3. Conditional Greeting Result Display
if st.session_state.greeting_data:
    data = st.session_state.greeting_data

    # ... (Keep the <style> block exactly as it is) ...

    # The entire result is now constructed in one HTML block inside the st.container
    with st.container():
        
        # --- FIXED CODE: Combine everything into one string ---
        html_content = f"""
        <div class="result-box">
            <p class="greeting-style">{data["greeting_line"]}</p>
            <h2 class="name-style">{data["full_name"]}</h2>
            <p class="age-style">{data["age_line"]}</p>
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
        # -----------------------------------------------------