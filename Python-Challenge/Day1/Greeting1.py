import streamlit as st
import datetime
import random 

# --- Configuration and Utility Functions ---

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
    
    challenge_greeting = "Welcome to Social Eagle Batch-3 Day 1 Python Challenge!"
    
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

# --- Floating Balloons CSS and Generation ---
num_balloons = 15 # Number of floating balloons

balloon_html = ""
for i in range(num_balloons):
    start_x = random.randint(0, 100) # Starting X position (percentage)
    animation_delay = random.uniform(0, 10) # Animation delay for staggered effect
    animation_duration = random.uniform(15, 25) # How long each balloon animation lasts (slower than flowers)
    balloon_size = random.randint(25, 45) # Size of the balloon emoji in pixels
    # Changed to balloon emojis
    balloon_emoji = random.choice(["🎈", "🎉", "🎊", "🎁"]) 
    
    balloon_html += f"""
    <div class="balloon" style="
        left: {start_x}vw; 
        animation-delay: {animation_delay}s;
        animation-duration: {animation_duration}s;
        font-size: {balloon_size}px;
    ">
        {balloon_emoji}
    </div>
    """

# Add the CSS for floating balloons and the existing styles
st.markdown(f"""
    <style>
    /* General body styling for background (optional, can be removed if not desired) */
    body {{
        background-color: #f8f9fa; /* Light background for contrast */
    }}

    /* CSS for the floating balloons (Modified 'float' keyframes for balloon-like sway) */
    @keyframes balloon-float {{
        0% {{
            transform: translateY(0) translateX(0) rotate(0deg);
            opacity: 0.9;
        }}
        25% {{
            transform: translateY(-20vh) translateX(3vw) rotate(2deg);
            opacity: 0.8;
        }}
        50% {{
            transform: translateY(-40vh) translateX(-3vw) rotate(-2deg);
            opacity: 0.7;
        }}
        75% {{
            transform: translateY(-60vh) translateX(3vw) rotate(2deg);
            opacity: 0.6;
        }}
        100% {{
            transform: translateY(-100vh) translateX(0vw) rotate(0deg);
            opacity: 0;
        }}
    }}

    .balloon {{
        position: fixed;
        top: 100vh; /* Start from bottom of the viewport */
        pointer-events: none; /* Allows clicks to pass through */
        animation-name: balloon-float; /* Use the new keyframe name */
        animation-iteration-count: infinite;
        animation-timing-function: linear;
        z-index: 9999; /* Ensure balloons are on top */
    }}

    /* Existing result box styles */
    .result-box {{
        background-color: #f0f2f6; /* Light gray background */
        padding: 30px;
        border-radius: 10px;
        border: 2px solid #43a047; /* Light green border */
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 20px;
    }}
    .name-style {{
        color: #6a1b9a; /* Purple */
        font-size: 40px;
        font-family: 'Georgia', serif;
        margin-bottom: 10px;
    }}
    .age-style {{
        color: #1b5e20; /* Dark green */
        font-size: 20px;
        margin-bottom: 20px;
    }}
    .greeting-style {{
        color: #43a047; /* Light green */
        font-size: 24px;
        font-style: italic;
        font-weight: bold;
    }}
    </style>
    {balloon_html} 
""", unsafe_allow_html=True)


# --- Sidebar Input Form ---
with st.sidebar:
    st.header("👤 Your Details")
    st.markdown("---")

    with st.form(key='user_form'):
        st.subheader("Names")
        st.text_input(
            label="First Name",
            key="first_name_input",
            placeholder="e.g., John",
            max_chars=50,
            help="Press Enter inside the text box to easily submit the form.", 
            label_visibility='collapsed' 
        )
        st.text_input(
            label="Last Name",
            key="last_name_input",
            placeholder="e.g., Doe",
            max_chars=50,
            help="Press Enter inside the text box to easily submit the form.",
            label_visibility='collapsed'
        )
        
        st.markdown("---")

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

        st.form_submit_button(
            label="Generate Greeting ✨",
            on_click=generate_greeting_message,
            type="primary",
            use_container_width=True
        )

    st.markdown("---")
    st.caption(f"App by Social Eagle Batch-3 | {datetime.datetime.now().year}")

# --- Main Page Display (Header and Result) ---

st.title("🦅 Social Eagle Challenge Greeting")
st.markdown("#### Personalized welcome for Day 1 participants.")
st.markdown("---")


# 2. Status/Error Message Display
if st.session_state.message_type == "error":
    st.error(st.session_state.message_content, icon="❌") # CORRECTED
elif st.session_state.message_type == "success":
    st.success(st.session_state.message_content, icon="🎉") # CORRECTED
else:
    st.info(st.session_state.message_content, icon="ℹ️")

# 3. Conditional Greeting Result Display
if st.session_state.greeting_data:
    data = st.session_state.greeting_data

    with st.container():
        html_content = f"""
        <div class="result-box">
            <p class="greeting-style">{data["greeting_line"]}</p>
            <h2 class="name-style">{data["full_name"]}</h2>
            <p class="age-style">{data["age_line"]}</p>
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)