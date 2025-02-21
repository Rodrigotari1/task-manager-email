import streamlit as st
import requests
from datetime import datetime
from app.streamlit.config import settings

st.set_page_config(
    page_title="Task Manager",
    page_icon="✅",
    layout="wide"
)

def main():
    st.title("Task Manager")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Tasks", "Email Tracking"])
    
    if page == "Tasks":
        show_tasks_page()
    else:
        show_email_tracking_page()

def show_tasks_page():
    st.header("Tasks")
    
    # Add new task
    with st.form("new_task"):
        st.subheader("Add New Task")
        title = st.text_input("Title")
        description = st.text_area("Description")
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        due_date = st.date_input("Due Date")
        notify = st.checkbox("Send email notification")
        
        if st.form_submit_button("Add Task"):
            try:
                # Here we'll add the API call to create task
                st.success("Task added successfully!")
            except Exception as e:
                st.error(f"Error adding task: {str(e)}")

def show_email_tracking_page():
    st.header("Email Tracking")
    
    try:
        # Get analytics
        response = requests.get(f"{settings.EMAIL_SERVICE_URL}/api/v1/tracking/analytics")
        analytics = response.json()
        
        # Display analytics in columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sent", analytics["total_sent"])
        with col2:
            st.metric("Open Rate", f"{analytics['open_rate']:.1f}%")
        with col3:
            st.metric("Click Rate", f"{analytics['click_rate']:.1f}%")
        with col4:
            st.metric("Delivery Rate", f"{analytics['delivery_rate']:.1f}%")
            
        # Recent events
        st.subheader("Recent Email Events")
        # Here we'll add a table of recent events
        
    except Exception as e:
        st.error(f"Error fetching email analytics: {str(e)}")

if __name__ == "__main__":
    main() 