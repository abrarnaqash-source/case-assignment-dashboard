import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="📋 Support Team Case Tracker", layout="wide")

# ---- Session State ----
if "team" not in st.session_state:
    st.session_state.team = ["Alice", "Bob", "Charlie", "David"]
if "working_today" not in st.session_state:
    st.session_state.working_today = []
if "cases" not in st.session_state:
    st.session_state.cases = pd.DataFrame(columns=["Case ID", "Assigned To", "Time", "Status"])

# ---- Helper: Colored Badge ----
def badge(text, color):
    return f"<span style='background-color:{color}; color:white; padding:4px 8px; border-radius:8px; font-size:90%'>{text}</span>"

# ---- Title ----
st.markdown("<h1 style='color:#4CAF50;'>📋 Support Team Case Tracker</h1>", unsafe_allow_html=True)
st.write("Track team availability, manual case assignments, and workload distribution.")

# ---- Sidebar: Team Availability ----
with st.sidebar:
    st.header("👥 Team Availability")
    st.session_state.working_today = st.multiselect(
        "Select team members working today:",
        st.session_state.team,
        default=st.session_state.working_today
    )

    # Add new team member
    new_member = st.text_input("➕ Add New Team Member")
    if st.button("Add Member") and new_member:
        if new_member not in st.session_state.team:
            st.session_state.team.append(new_member)
            st.success(f"Added {new_member}")
        else:
            st.warning(f"{new_member} is already in the team.")

# ---- Manual Case Assignment ----
st.subheader("📝 Assign a Case")
case_id = st.text_input("Enter Case ID")
assigned_to = st.selectbox("Assign To", options=st.session_state.working_today)
status = st.selectbox("Case Status", ["Open", "In Progress", "Closed"])

if st.button("Assign Case"):
    if not case_id:
        st.error("Please enter a Case ID.")
    elif not assigned_to:
        st.error("Please select a team member who is working today.")
    else:
        new_case = pd.DataFrame(
            [[case_id, assigned_to, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), status]],
            columns=["Case ID", "Assigned To", "Time", "Status"]
        )
        st.session_state.cases = pd.concat([st.session_state.cases, new_case], ignore_index=True)
        st.success(f"✅ Case {case_id} assigned to {assigned_to}")

# ---- Display: Who is working today ----
st.subheader("👨‍💻 Working Today")
if st.session_state.working_today:
    st.markdown(
        " ".join([badge(member, "#2196F3") for member in st.session_state.working_today]),
        unsafe_allow_html=True
    )
else:
    st.warning("No one is marked as working today.")

# ---- Filters ----
if not st.session_state.cases.empty:
    st.subheader("🔍 Filter Cases")
    filter_member = st.multiselect("Filter by Team Member", options=st.session_state.team)
    filter_status = st.multiselect("Filter by Status", options=["Open", "In Progress", "Closed"])

    filtered_df = st.session_state.cases.copy()
    if filter_member:
        filtered_df = filtered_df[filtered_df["Assigned To"].isin(filter_member)]
    if filter_status:
        filtered_df = filtered_df[filtered_df["Status"].isin(filter_status)]

    # ---- Display: Case Tracking ----
    st.subheader("📂 Case Assignments")
    styled_df = filtered_df.style.applymap(
        lambda val: "background-color: #FF9800; color: white;" if val == "In Progress"
        else "background-color: #4CAF50; color: white;" if val == "Open"
        else "background-color: #9E9E9E; color: white;" if val == "Closed"
        else "",
        subset=["Status"]
    )
    st.dataframe(styled_df, use_container_width=True)

    # ---- Summary: Cases per Person ----
    st.subheader("📊 Workload Summary")
    summary = filtered_df["Assigned To"].value_counts().reset_index()
    summary.columns = ["Team Member", "Cases Assigned"]
    st.table(summary)

    # ---- Bar Chart ----
    st.bar_chart(summary.set_index("Team Member"))
else:
    st.info("No cases assigned yet.")
