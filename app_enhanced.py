import streamlit as st
import pandas as pd
import json
from data_manager import DataManager
import io

# Page configuration
st.set_page_config(
    page_title="Project Management System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize data manager
@st.cache_resource
def get_data_manager():
    return DataManager()

dm = get_data_manager()

# Sidebar for JSON service file upload
st.sidebar.title("Configuration")
st.sidebar.markdown("### Google Cloud Service Account")

uploaded_file = st.sidebar.file_uploader(
    "Upload JSON Service Account Key",
    type=['json'],
    help="Upload your Google Cloud service account JSON file for Google Sheets integration"
)

if uploaded_file is not None:
    try:
        service_account_info = json.load(uploaded_file)
        st.sidebar.success("✅ Service account file uploaded successfully!")
        st.sidebar.json({"project_id": service_account_info.get("project_id", "N/A")})
    except Exception as e:
        st.sidebar.error(f"❌ Error reading JSON file: {str(e)}")

# Main application
st.title("📊 Project Management System")
st.markdown("---")

# Load data with refresh capability
def load_all_data():
    return {
        'projects': dm.load_projects(),
        'tasks': dm.load_tasks(),
        'clients': dm.load_clients(),
        'teams': dm.load_teams()
    }

# Initialize session state for data refresh
if 'data_refresh' not in st.session_state:
    st.session_state.data_refresh = 0

data = load_all_data()

# Navigation tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Dashboard", "🏗️ Projects", "✅ Tasks", "👥 Clients", "🔧 Teams"])

with tab1:
    st.header("Dashboard Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Projects", len(data['projects']))
    
    with col2:
        st.metric("Total Tasks", len(data['tasks']))
    
    with col3:
        st.metric("Active Clients", len(data['clients']))
    
    with col4:
        st.metric("Team Members", len(data['teams']))
    
    # Project status distribution
    st.subheader("Project Status Distribution")
    project_status_counts = data['projects']['Status'].value_counts()
    st.bar_chart(project_status_counts)
    
    # Task status distribution
    st.subheader("Task Status Distribution")
    task_status_counts = data['tasks']['Status'].value_counts()
    st.bar_chart(task_status_counts)

with tab2:
    st.header("Projects Management")
    
    # Add new project form
    with st.expander("➕ Add New Project"):
        with st.form("new_project_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                project_name = st.text_input("Project Name")
                status = st.selectbox("Status", ["Not Started", "In Progress", "Completed", "On Hold"])
                assigned_to = st.selectbox("Assigned To", data['teams']['Team Member Name'].tolist())
            
            with col2:
                description = st.text_area("Description")
                due_date = st.date_input("Due Date")
                client_name = st.selectbox("Client", data['clients']['Client Name'].tolist())
            
            submitted = st.form_submit_button("Add Project")
            
            if submitted and project_name:
                project_data = {
                    'Project Name': project_name,
                    'Description': description,
                    'Status': status,
                    'Due Date': due_date.strftime('%Y-%m-%d'),
                    'Assigned To': assigned_to,
                    'Client Name': client_name
                }
                dm.add_project(project_data)
                st.success(f"Project '{project_name}' has been added successfully!")
                st.session_state.data_refresh += 1
                st.rerun()
    
    # Display projects with delete functionality
    st.subheader("Current Projects")
    projects_df = data['projects']
    
    # Add delete buttons
    for idx, row in projects_df.iterrows():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{row['Project Name']}** - {row['Status']} - Due: {row['Due Date']}")
        with col2:
            if st.button(f"🗑️ Delete", key=f"del_proj_{idx}"):
                dm.delete_project(idx)
                st.success(f"Project '{row['Project Name']}' deleted!")
                st.session_state.data_refresh += 1
                st.rerun()
    
    st.dataframe(projects_df, use_container_width=True)
    
    # Export projects to CSV
    if st.button("📥 Export Projects to CSV"):
        csv_buffer = io.StringIO()
        projects_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download Projects CSV",
            data=csv_buffer.getvalue(),
            file_name="projects_export.csv",
            mime="text/csv"
        )

with tab3:
    st.header("Tasks Management")
    
    # Add new task form
    with st.expander("➕ Add New Task"):
        with st.form("new_task_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                task_name = st.text_input("Task Name")
                project_name = st.selectbox("Project", data['projects']['Project Name'].tolist())
                status = st.selectbox("Status", ["To Do", "Doing", "Done"])
            
            with col2:
                description = st.text_area("Description")
                due_date = st.date_input("Due Date")
                assigned_to = st.selectbox("Assigned To", data['teams']['Team Member Name'].tolist())
            
            submitted = st.form_submit_button("Add Task")
            
            if submitted and task_name:
                task_data = {
                    'Task Name': task_name,
                    'Project Name': project_name,
                    'Description': description,
                    'Status': status,
                    'Due Date': due_date.strftime('%Y-%m-%d'),
                    'Assigned To': assigned_to
                }
                dm.add_task(task_data)
                st.success(f"Task '{task_name}' has been added successfully!")
                st.session_state.data_refresh += 1
                st.rerun()
    
    # Display tasks with delete functionality
    st.subheader("Current Tasks")
    tasks_df = data['tasks']
    
    # Add delete buttons
    for idx, row in tasks_df.iterrows():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{row['Task Name']}** - {row['Status']} - Project: {row['Project Name']}")
        with col2:
            if st.button(f"🗑️ Delete", key=f"del_task_{idx}"):
                dm.delete_task(idx)
                st.success(f"Task '{row['Task Name']}' deleted!")
                st.session_state.data_refresh += 1
                st.rerun()
    
    st.dataframe(tasks_df, use_container_width=True)
    
    # Export tasks to CSV
    if st.button("📥 Export Tasks to CSV"):
        csv_buffer = io.StringIO()
        tasks_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download Tasks CSV",
            data=csv_buffer.getvalue(),
            file_name="tasks_export.csv",
            mime="text/csv"
        )

with tab4:
    st.header("Clients Management")
    
    # Add new client form
    with st.expander("➕ Add New Client"):
        with st.form("new_client_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                client_name = st.text_input("Client Name")
                contact_person = st.text_input("Contact Person")
                email = st.text_input("Email")
            
            with col2:
                phone = st.text_input("Phone")
                company = st.text_input("Company")
                address = st.text_area("Address")
            
            submitted = st.form_submit_button("Add Client")
            
            if submitted and client_name:
                client_data = {
                    'Client Name': client_name,
                    'Contact Person': contact_person,
                    'Email': email,
                    'Phone': phone,
                    'Company': company,
                    'Address': address
                }
                dm.add_client(client_data)
                st.success(f"Client '{client_name}' has been added successfully!")
                st.session_state.data_refresh += 1
                st.rerun()
    
    # Display clients with delete functionality
    st.subheader("Current Clients")
    clients_df = data['clients']
    
    # Add delete buttons
    for idx, row in clients_df.iterrows():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{row['Client Name']}** - {row['Contact Person']} - {row['Email']}")
        with col2:
            if st.button(f"🗑️ Delete", key=f"del_client_{idx}"):
                dm.delete_client(idx)
                st.success(f"Client '{row['Client Name']}' deleted!")
                st.session_state.data_refresh += 1
                st.rerun()
    
    st.dataframe(clients_df, use_container_width=True)
    
    # Export clients to CSV
    if st.button("📥 Export Clients to CSV"):
        csv_buffer = io.StringIO()
        clients_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download Clients CSV",
            data=csv_buffer.getvalue(),
            file_name="clients_export.csv",
            mime="text/csv"
        )

with tab5:
    st.header("Teams Management")
    
    # Add new team member form
    with st.expander("➕ Add New Team Member"):
        with st.form("new_team_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                member_name = st.text_input("Team Member Name")
                role = st.text_input("Role")
                email = st.text_input("Email")
            
            with col2:
                phone = st.text_input("Phone")
                department = st.text_input("Department")
                status = st.selectbox("Status", ["Active", "Inactive"])
            
            submitted = st.form_submit_button("Add Team Member")
            
            if submitted and member_name:
                team_data = {
                    'Team Member Name': member_name,
                    'Role': role,
                    'Email': email,
                    'Phone': phone,
                    'Department': department,
                    'Status': status
                }
                dm.add_team_member(team_data)
                st.success(f"Team member '{member_name}' has been added successfully!")
                st.session_state.data_refresh += 1
                st.rerun()
    
    # Display team members with delete functionality
    st.subheader("Current Team Members")
    teams_df = data['teams']
    
    # Add delete buttons
    for idx, row in teams_df.iterrows():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{row['Team Member Name']}** - {row['Role']} - {row['Department']}")
        with col2:
            if st.button(f"🗑️ Delete", key=f"del_team_{idx}"):
                dm.delete_team_member(idx)
                st.success(f"Team member '{row['Team Member Name']}' deleted!")
                st.session_state.data_refresh += 1
                st.rerun()
    
    st.dataframe(teams_df, use_container_width=True)
    
    # Export teams to CSV
    if st.button("📥 Export Teams to CSV"):
        csv_buffer = io.StringIO()
        teams_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download Teams CSV",
            data=csv_buffer.getvalue(),
            file_name="teams_export.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("### 🔗 Integration Status")
col1, col2, col3 = st.columns(3)

with col1:
    st.info("📊 **Google Sheets**: Ready for integration")

with col2:
    st.info("🔗 **n8n Webhooks**: Ready for integration")

with col3:
    st.info("🎤 **VAPI Voice**: Ready for integration")

