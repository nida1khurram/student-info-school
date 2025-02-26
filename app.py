
import streamlit as st
import pandas as pd
import os

# File path for saving data
DATA_FILE = "students_data.csv"

# Load existing data from CSV (if the file exists)
if os.path.exists(DATA_FILE):
    st.session_state.students = pd.read_csv(DATA_FILE)
else:
    st.session_state.students = pd.DataFrame(columns=[
        'ID', 'Name', 'Age', 'Class', 'Phone', 'Address', 'Parent Info'
    ])

# Function to save data to CSV
def save_data():
    st.session_state.students.to_csv(DATA_FILE, index=False)

# Function to add a new student
def add_student(id, name, age, student_class, phone, address, parent_info):
    new_student = pd.DataFrame([[
        id, name, age, student_class, phone, address, parent_info
    ]], columns=['ID', 'Name', 'Age', 'Class', 'Phone', 'Address', 'Parent Info'])
    st.session_state.students = pd.concat([st.session_state.students, new_student], ignore_index=True)
    save_data()  # Save data after adding

# Function to filter students
def filter_students(filter_by, filter_value):
    if filter_by == 'ID':
        return st.session_state.students[st.session_state.students['ID'] == int(filter_value)]
    elif filter_by == 'Name':
        return st.session_state.students[st.session_state.students['Name'].str.contains(filter_value, case=False)]
    elif filter_by == 'Class':
        return st.session_state.students[st.session_state.students['Class'] == filter_value]
    else:
        return st.session_state.students

# Function to modify student information
def modify_student(id, name, age, student_class, phone, address, parent_info):
    index = st.session_state.students[st.session_state.students['ID'] == id].index
    if not index.empty:
        st.session_state.students.at[index[0], 'Name'] = name
        st.session_state.students.at[index[0], 'Age'] = age
        st.session_state.students.at[index[0], 'Class'] = student_class
        st.session_state.students.at[index[0], 'Phone'] = phone
        st.session_state.students.at[index[0], 'Address'] = address
        st.session_state.students.at[index[0], 'Parent Info'] = parent_info
        save_data()  # Save data after modifying

# Streamlit UI
st.title("Student Information System (SIS)")

# Sidebar for navigation
menu = st.sidebar.selectbox("Menu", ["Add Student", "View Students", "Filter Students", "Modify Student"])

if menu == "Add Student":
    st.header("Add New Student")
    id = st.number_input("ID", min_value=1, step=1)
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, step=1)
    student_class = st.text_input("Class")
    phone = st.text_input("Phone Number")
    address = st.text_input("Address")
    parent_info = st.text_input("Parent Information")
    if st.button("Add Student"):
        add_student(id, name, age, student_class, phone, address, parent_info)
        st.success("Student added successfully!")

elif menu == "View Students":
    st.header("View All Students")
    st.dataframe(st.session_state.students)

elif menu == "Filter Students":
    st.header("Filter Students")
    filter_by = st.selectbox("Filter By", ["ID", "Name", "Class"])
    filter_value = st.text_input("Filter Value")
    if st.button("Filter"):
        filtered_students = filter_students(filter_by, filter_value)
        st.dataframe(filtered_students)

elif menu == "Modify Student":
    st.header("Modify Student Information")
    id = st.number_input("Enter Student ID to Modify", min_value=1, step=1)
    name = st.text_input("New Name")
    age = st.number_input("New Age", min_value=1, step=1)
    student_class = st.text_input("New Class")
    phone = st.text_input("New Phone Number")
    address = st.text_input("New Address")
    parent_info = st.text_input("New Parent Information")
    if st.button("Modify Student"):
        modify_student(id, name, age, student_class, phone, address, parent_info)
        st.success("Student information modified successfully!")

# run file
# streamlit run app.py