import streamlit as st
import pandas as pd
from datetime import datetime

# Streamlit page settings
st.set_page_config(page_title="🎯 Case Assignment Dashboard", layout="wide")

# Initialize session state variables
if "team" not in st.session_state:
    st.session_state.team = ["Alice", "Bob", "Charlie"]  # Default team members
if "next_index" not in st.session_state:
    st.session_state.next_index = 0  # For round robin tracking
if "cases" not in st.session_state:
    st.session_state.cases = pd.DataFrame(columns=["Case ID", "Assigned To", "Time", "Status"])

# App title
st.title("🎯 Case Assignment Dashboard")
st.write("Assign cases in a round robin fashion and track them live.")

# Sidebar for team management
with st.sidebar:
    st.header("👥 Team Settings")
    new_member = st.text_input("Add Team Member")
    if st.button("Add Member") and new_member:
        if new_member not in st.session_state.team:
            st.session_state.team.append(new_member)
            st.success(f"Added {new_member}")
        else:
            st.warning(f"{new_member} is already in the team.")

    remove_member = st.selectbox("Remove Team Member", [""] + st.session_state.team)
    if st.button("Remove Member") and remove_member:
        st.session_state.team.remove(remove_member)
        st.success(f"Removed {remove_member}")

# Input for case assignment
case_id = st.text_input("Enter Case ID")
if st.button("Assign Case") and case_id:
    if not st.session_state.team:
        st.error("No team members available to assign cases.")
    else:
        assigned_to = st.session_state.team[st.session_state.next_index]
        st.session_state.next_index = (st.session_state.next_index + 1) % len(st.session_state.team)

        # Add case to tracking table
        new_case = pd.DataFrame([[case_id, assigned_to, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Open"]],
                                columns=["Case ID", "Assigned To", "Time", "Status"])
        st.session_state.cases = pd.concat([st.session_state.cases, new_case], ignore_index=True)

        st.success(f"✅ Case {case_id} assigned to {assigned_to}")

# Display case tracking table
st.subheader("📋 Case Tracking")
st.dataframe(st.session_state.cases)

# Workload distribution chart
if not st.session_state.cases.empty:
    st.subheader("📊 Workload Distribution")
    workload = st.session_state.cases["Assigned To"].value_counts()
    st.bar_chart(workload)
