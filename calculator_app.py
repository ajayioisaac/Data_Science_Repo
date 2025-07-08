import streamlit as st
st.title("Simple Calculator")
st.text("This is a simple calculator to perform basic arithmetical operations")

first_number = st.number_input("Enter the first number")
second_number = st.number_input("Enter the second number")
operation = st.selectbox("Select an operation:", ["Addition", "Subtraction", "Multiplication", "Division"])


# Calculate button
if st.button("calculate"):
    if operation == "Addition":
        result = first_number + second_number
        st.success(f"The result is: {result}")
    elif operation == "Subtraction":
        result = first_number - second_number
        st.success(f"The result is: {result}")
    elif operation == "Multiplication":
        result = first_number * second_number
        st.success(f"The result is: {result}")
    elif operation == "Division":
        if second_number != 0:
            result = first_number/second_number
            st.success(f"The result is: {result}")
        else:
            st.error("Division by zero is not allowed. Please enter a non-zero second number")
        

