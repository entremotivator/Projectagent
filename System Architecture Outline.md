# System Architecture Outline

## 1. Overview
This project aims to develop a one-page Streamlit application for project management, integrating with n8n for webhook automation, VAPI for voice interaction, and Google Sheets as the live data source. The system will also provide functionality to export project data to CSV, and manage clients and teams, with notification features.

## 2. Components

### 2.1. Streamlit Application (Frontend)
- **Purpose:** User interface for project management (viewing, adding, editing projects/tasks, managing clients and teams).
- **Key Features:**
    - Display project list from Google Sheets.
    - Form for adding new projects/tasks.
    - Functionality to edit existing project/task details.
    - Management interfaces for Clients and Teams.
    - Button to trigger CSV export.
    - Integration with VAPI for voice commands.

### 2.2. Google Sheets (Data Source)
- **Purpose:** Centralized, live data storage for all project management data, including clients and teams.
- **Structure:**
    - Dedicated sheets for 'Projects', 'Tasks', 'Clients', and 'Teams'.
    - **'Projects' Sheet:** Columns for project name, description, status, due date, assigned to, etc.
    - **'Tasks' Sheet:** Columns for task name, project name (to link to Projects tab), description, status, due date, assigned to, etc.
    - **'Clients' Sheet:** Columns for client name, contact person, email, phone, etc.
    - **'Teams' Sheet:** Columns for team member name, role, contact info, etc.
    - Accessible via Streamlit using `st.connection` and `gspread`.

### 2.3. n8n (Webhook Automation & Notifications)
- **Purpose:** Handle automated workflows triggered by webhooks, e.g., notifications, data synchronization.
- **Workflow Examples:**
    - Triggered by Streamlit (e.g., on new project creation, task status change, or new client/team member added).
    - Send notifications (email, Slack, etc.) based on project/task updates, due date reminders, or new assignments.
    - Potentially update other systems.

### 2.4. VAPI Python Voice Agent (Voice Interface)
- **Purpose:** Enable voice-controlled interaction with the Streamlit application.
- **Functionality:**
    - Receive voice commands (e.g., "add new project", "update task status", "add new client", "assign task to team member").
    - Convert voice to text for processing.
    - Interact with Streamlit backend or Google Sheets directly based on commands.
    - Provide voice feedback to the user.

### 2.5. CSV Export Functionality
- **Purpose:** Allow users to download project, task, client, and team data in CSV format.
- **Implementation:**
    - Read data from Google Sheets (Projects, Tasks, Clients, Teams).
    - Convert data to pandas DataFrames.
    - Export DataFrames to CSV.
    - Provide download buttons in Streamlit.

## 3. Data Flow
1. User interacts with Streamlit UI.
2. Streamlit reads/writes data to Google Sheets (Projects, Tasks, Clients, Teams).
3. Streamlit sends webhooks to n8n for automated tasks and notifications.
4. VAPI voice agent receives voice input, processes it, and interacts with Streamlit/Google Sheets.
5. Streamlit generates CSV from Google Sheets data for download.

## 4. Deployment
- Streamlit application will be a local deployment.
- n8n instance (local or cloud-hosted).
- VAPI voice agent (local Python script).
- Google Sheets (cloud-based).

## 5. Technologies Used
- **Frontend:** Streamlit
- **Backend/Automation:** Python, n8n, VAPI SDK
- **Database:** Google Sheets
- **Libraries:** `gspread`, `pandas`, `streamlit-gsheets`, `vapi-python` (or similar)


