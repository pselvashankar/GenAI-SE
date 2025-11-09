import streamlit as st

st.title("This is my first Streamlit app!")

name=st.text_input("Enter your name:")

if st.button("Submit"):
    if name:
        st.success(f"Hello, {name}!, welcome to Streamlit page.")

    else:
        st.write("Please enter your name.")