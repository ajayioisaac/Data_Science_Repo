import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
st.title("Loan Prediction Dashboard")
st.header("Loan Prediction Dashboard")
st.subheader("This is a simple loan prediction dashboard built with Streamlit.")

## Text
st.text("This is a simple text.")
st.markdown("This is **bold** text and *italic* text.")
st.latex(r"""
\int_0^\infty e^{-x} \, dx = 1
""")
st.code("print('Hello, World!')", language='python')
st.write("This is a write function that can display text, data, and more.")

## Input Elements

## Text input
name = st.text_input("Enter your name:")
message = st.text_area("Enter your message:", height=100)

## Number input
age = st.number_input("Enter your age:", min_value=0, max_value=120, value=25)
slider_value = st.slider("Select a value:", min_value=0, max_value=100, value=50)

## Selectbox and Multiselect
option = st.selectbox("Select an option:", ["Option 1", "Option 2", "Option 3"])
options = st.multiselect("Select multiple options:", ["Option A", "Option B", "Option C"])
radio_choice = st.radio("Choose one option:", ["Choice 1", "Choice 2", "Choice 3"])
## Checkbox and Button
checkbox = st.checkbox("Check this box")

# Date and time
date = st.date_input("Select a date:")
time = st.time_input("Select a time:")

# File uploader
uploaded_file = st.file_uploader("Upload a file", type=["csv", "txt", "xlsx", "pdf"])

# Display elements
df = pd.DataFrame({
    "Column 1": [1, 2, 3],
    "Column 2": [4, 5, 6]
})
st.dataframe(df)
st.table(df)    
st.json({"name": "John", "age": 30, "city": "New York"})

# Charts
st.line_chart([1, 2, 3, 4, 5])
st.bar_chart([10, 20, 30, 40, 50])
st.area_chart([5, 10, 15, 20, 25])

# Media elements
st.image("data:image/png;base64,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" ,caption="Sample Image")
st.video("https://www.youtube.com/watch?v=HJOXl5zsUnU")

# Status elements
st.success("This is a success message!")
st.error("This is an error message!")
st.warning("This is a warning message!")
st.info("This is an informational message!")

# Progress and spinner
progress = st.progress(0)
for i in range(100):
   progress.progress(i + 1)
with st.spinner("Loading..."):
    import time
    time.sleep(10)  # Simulate a long computation
st.success("Done!")

# Layout and styling 
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Column 1")
    st.write("This is the first column.")

with col2:
    st.header("Column 2")
    st.write("This is the second column.")

with col3:
    st.header("Column 3")
    st.write("This is the third column.")
    data = pd.DataFrame({
        "x": range(1,11),
        "y": [x**2 for x in range(1, 11)]
    })
    fig, ax= plt.subplots()
    ax.plot(data["x"], data["y"])
    st.pyplot(fig)

# Sidebar
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Go to:", ["Home", "About", "Contact"])
# st.sidebar.info("This is the sidebar where you can add navigation links or other information.")

# container and expandable sections
container = st.container()
container.write("This is a container section where you can group related elements.")

with st.expander("Click to expand"):
    st.write("This is the expanded section.")
    st.text_input("Enter some text:")   