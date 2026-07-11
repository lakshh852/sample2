import streamlit as st
import pandas as pd
import os

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="Attendance Management System",
    page_icon="📚",
    layout="wide"
)

# ------------------------------
# Create CSV Files if Not Exists
# ------------------------------
if not os.path.exists("students.csv"):
    students = pd.DataFrame(columns=[
        "Student_ID",
        "Student_Name",
        "Department",
        "Year"
    ])
    students.to_csv("students.csv", index=False)

if not os.path.exists("attendance.csv"):
    attendance = pd.DataFrame(columns=[
        "Student_ID",
        "Student_Name",
        "Date",
        "Time",
        "Status"
    ])
    attendance.to_csv("attendance.csv", index=False)

# ------------------------------
# Sidebar
# ------------------------------
st.sidebar.title("📚 Attendance Management")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Add Student",
        "View Students",
        "Mark Attendance",
        "View Attendance"
    ]
)

# ------------------------------
# Home Page
# ------------------------------
if menu == "Home":

    st.title("📚 Attendance Management System")

    st.markdown("---")

    st.subheader("Welcome!")

    st.write(
        """
        This project helps you manage student attendance easily.

        ### Features
        - Add Student
        - View Students
        - Mark Attendance
        - View Attendance
        - Export Attendance (Coming Soon)
        """
    )

    students = pd.read_csv("students.csv")
    attendance = pd.read_csv("attendance.csv")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Students", len(students))

    with col2:
        st.metric("Attendance Records", len(attendance))

# ------------------------------
# Add Student
# ------------------------------
elif menu == "Add Student":

    st.header("➕ Add Student")

    sid = st.text_input("Student ID")
    name = st.text_input("Student Name")
    dept = st.text_input("Department")
    year = st.selectbox(
        "Year",
        ["I", "II", "III", "IV"]
    )

    if st.button("Save Student"):

        students = pd.read_csv("students.csv")

        new_student = pd.DataFrame({
            "Student_ID": [sid],
            "Student_Name": [name],
            "Department": [dept],
            "Year": [year]
        })

        students = pd.concat(
            [students, new_student],
            ignore_index=True
        )

        students.to_csv("students.csv", index=False)

        st.success("Student Added Successfully!")

# ------------------------------
# View Students
# ------------------------------
elif menu == "View Students":

    st.header("👨‍🎓 Student List")

    students = pd.read_csv("students.csv")

    st.dataframe(students, use_container_width=True)

# ------------------------------
# Mark Attendance
# ------------------------------
elif menu == "Mark Attendance":

    st.header("✅ Mark Attendance")

    students = pd.read_csv("students.csv")

    if students.empty:
        st.warning("No students available.")
    else:

        student = st.selectbox(
            "Select Student",
            students["Student_Name"]
        )

        status = st.radio(
            "Attendance",
            ["Present", "Absent"]
        )

        if st.button("Submit Attendance"):

            row = students[
                students["Student_Name"] == student
            ].iloc[0]

            attendance = pd.read_csv("attendance.csv")

            new_record = pd.DataFrame({
                "Student_ID": [row["Student_ID"]],
                "Student_Name": [row["Student_Name"]],
                "Date": [pd.Timestamp.now().strftime("%d-%m-%Y")],
                "Time": [pd.Timestamp.now().strftime("%I:%M %p")],
                "Status": [status]
            })

            attendance = pd.concat(
                [attendance, new_record],
                ignore_index=True
            )

            attendance.to_csv("attendance.csv", index=False)

            st.success("Attendance Saved!")

# ------------------------------
# View Attendance
# ------------------------------
elif menu == "View Attendance":

    st.header("📋 Attendance Records")

    attendance = pd.read_csv("attendance.csv")

    st.dataframe(attendance, use_container_width=True)
