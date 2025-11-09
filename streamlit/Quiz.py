import streamlit as st
import random

# --- Quiz Data ---
# Structure: Question, options (list), correct answer (string)
QUIZ_QUESTIONS = [
    {
        "question": "What is the capital of Australia?",
        "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
        "answer": "Canberra"
    },
    {
        "question": "Which planet is known as the 'Red Planet'?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "answer": "Mars"
    },
    {
        "question": "What is the square root of 64?",
        "options": ["6", "7", "8", "9"],
        "answer": "8"
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "answer": "Pacific"
    },
]

# --- Session State Initialization ---

def init_session_state():
    """Initializes or resets the required session state variables."""
    if 'question_index' not in st.session_state:
        st.session_state.question_index = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    # Use 'shuffled_questions' to ensure the order is fixed per session
    if 'shuffled_questions' not in st.session_state:
        # Create a shuffled copy of the questions list
        shuffled = QUIZ_QUESTIONS[:]
        random.shuffle(shuffled)
        st.session_state.shuffled_questions = shuffled

# --- Helper Functions ---

def submit_answer(current_question_index, selected_option):
    """
    Handles the submission of an answer: checks correctness, updates score,
    and moves to the next question.
    """
    if selected_option is None:
        st.warning("Please select an answer before submitting.")
        return

    question_data = st.session_state.shuffled_questions[current_question_index]
    correct_answer = question_data["answer"]

    # 1. Record the user's answer
    st.session_state.user_answers[current_question_index] = selected_option
    
    # Store feedback in state to display on the next run
    if selected_option == correct_answer:
        st.session_state.score += 1
        st.session_state.feedback = "Correct! ✅"
    else:
        st.session_state.feedback = f"Incorrect. The correct answer was: **{correct_answer}** ❌"

    # 2. Move to the next question
    st.session_state.question_index += 1
    
    # NOTE: The explicit call to st.rerun() is removed here, relying on 
    # Streamlit's automatic rerun after the callback finishes.


def restart_quiz():
    """Resets all session state variables to start the quiz over."""
    # This function resets the state when the "Restart Quiz" button is pressed
    st.session_state.clear()
    init_session_state()
    # NOTE: The explicit call to st.rerun() is removed here.

# --- Main App Logic ---

def main():
    """Renders the quiz application."""
    st.set_page_config(
        page_title="Streamlit Python Quiz",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    st.title("🐍 Streamlit General Knowledge Quiz")

    # Initialize the state on first load
    init_session_state()
    
    # Check if the quiz is over
    total_questions = len(st.session_state.shuffled_questions)
    current_index = st.session_state.question_index
    
    # Display and clear transient feedback if it exists (from the previous submission)
    if 'feedback' in st.session_state:
        st.info(st.session_state.feedback, icon="💡")
        del st.session_state.feedback # Clear after displaying

    if current_index >= total_questions:
        # --- End Screen ---
        st.balloons()
        
        st.header("Quiz Complete! 🎉")
        st.markdown(f"""
            ### Your Final Score: **{st.session_state.score} / {total_questions}**
        """)
        
        # Display feedback based on score
        if st.session_state.score == total_questions:
            st.success("Perfect score! You are a master of trivia!")
        elif st.session_state.score > total_questions / 2:
            st.info("Great job! You passed the quiz.")
        else:
            st.warning("You might want to review some general knowledge, but keep practicing!")

        # Show a button to restart
        st.button("Restart Quiz", on_click=restart_quiz)
            
    else:
        # --- Quiz In Progress ---
        
        # Display progress
        st.markdown(f"**Question {current_index + 1} of {total_questions}** | Score: {st.session_state.score}")
        st.progress((current_index + 1) / total_questions)

        # Get the current question data
        question_data = st.session_state.shuffled_questions[current_index]

        # Display the question
        st.subheader(f"{question_data['question']}")

        # Radio buttons for options. Key ensures the radio resets when question changes.
        selected_option = st.radio(
            "Select your answer:",
            question_data["options"],
            key=f"q_{current_index}",
            index=None # Starts with no option selected
        )
        
        st.markdown("---")

        # Submit button. Uses a lambda function to pass arguments to the callback.
        st.button(
            "Submit Answer",
            type="primary",
            on_click=submit_answer,
            args=(current_index, selected_option)
        )

# Run the main function
if __name__ == "__main__":
    main()